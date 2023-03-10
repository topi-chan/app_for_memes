import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from one_app.db.db import get_session
from one_app.db.meme_models import Meme
from one_app.db.meme_models import Meme as Meme_db
from one_app.schemas.memes import Meme as MemeSchema
from one_app.schemas.memes import MemeCreate
from one_app.services.memes import MemesService, datetime_now, split_memes
from one_app.orm import Session

router = APIRouter(tags=["memes"])


@router.get("/", response_model=list, status_code=200)
def get_memes(session: Session = Depends(get_session)):
    """Zwróc wszystkie memy"""
    memes = MemesService.get_memes(session=session)
    return memes


@router.get("/mem/{number}", response_model=list, status_code=200)
def get_sub_memes_by_date_add(number: int, session: Session = Depends(get_session)):
    """Zwróc listy zaakceptowanych memów wg zadanej wielkości listy, posegregowane wg date_mod"""
    memes = MemesService.get_memes_by_date(session=session)
    try:
        sublist = split_memes(memes, 20)[number]
    except IndexError:
        sublist = []
    return sublist


@router.get("/mem_like/{number}", response_model=list, status_code=200)
def get_sub_memes_by_like(number: int, session: Session = Depends(get_session)):
    """Zwróc listy zaakceptowanych memów wg zadanej wielkości listy, posegregowane wg like"""
    memes = MemesService.get_memes_by_like(session=session)
    try:
        sublist = split_memes(memes, 20)[number]
    except IndexError:
        sublist = []
    return sublist


@router.get("/best/{number}", response_model=list, status_code=200)
def get_best_sub_memes(number: int, session: Session = Depends(get_session)):
    """Zwróc listy najlepszych, zaakceptowanych memów wg zadanej wielkości listy, posegregowane wg daty"""
    memes = MemesService.get_best_memes(session=session)
    try:
        sublist = split_memes(memes, 20)[number]
    except IndexError:
        sublist = []
    return sublist


@router.get("/accepted_memes", response_model=list[MemeSchema], status_code=200)
def get_accepted_memes(session: Session = Depends(get_session)):
    """Zwróc listę wszystkich zaakceptowanych memów bez sortowania"""
    accepted_memes = MemesService.get_accepted_memes(session=session)
    return accepted_memes


@router.post("/", response_model=MemeSchema, status_code=200)
def post_meme(body: MemeCreate, session: Session = Depends(get_session)):
    """Utwórz obiekt mema w bazie - do poprawy / uzupełnienia"""
    meme = MemesService.create_meme(
        name=body.name,
        like=body.like,
        status_id=body.status_id,
        session=session,
    )
    return meme


@router.get("/{id}", response_model=MemeSchema, status_code=200)
def get_meme(id: str, session: Session = Depends(get_session)):
    """Zwróc mema jako obiekt z bazy, bez pliku binarnego"""
    meme = MemesService.get_meme(meme_id=id, session=session)
    if not meme:
        raise HTTPException(status_code=404, detail=f"Meme with id={id} not found!")
    return meme


@router.post("/send_meme", response_model=None)
async def send_meme(
    nick: str = Form(),
    alias: str = Form(),
    width: int = Form(),
    height: int = Form(),
    description: Optional[str] = Form(None),
    date_mod: Optional[datetime] = Form(None),
    date_add: Optional[datetime] = Form(datetime_now),
    file: UploadFile = File(),
    session: Session = Depends(get_session),
):
    """Wyślij mema jako obiekt binarny i zapisz obiekt w bazie"""
    fs = await file.read()
    uuid = uuid4()
    upload_dir = Path(f"/meme_save/{str(uuid)[0]}/{uuid}")
    upload_dir.mkdir(parents=True)
    if os.path.isfile(f"{upload_dir}/{file.filename}"):
        i = 0
        while os.path.exists(f"{upload_dir}/%s{file.filename}" % i):
            i += 1
        name = f"%s{file.filename}" % i
        with open(f"{upload_dir}/{name}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    else:
        name = file.filename
        with open(f"{upload_dir}/{name}", "wb") as buffer:
            buffer.write(fs)
    with session as session:
        meme = Meme(
            name=f"{upload_dir}/{name}",
            like=0,
            status_id=1,
            date_add=date_add,
            date_mod=date_mod,
            nick=nick,
            alias=alias,
            width=width,
            height=height,
            description=description,
        )
        session.add(meme)
        session.commit()
        session.flush()
    return 200


@router.get(
    "/show_meme/{id}",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
def get_meme(id: str, session: Session = Depends(get_session)):
    """Do poprawy/uzupełnienia - zwróć mema jako obiekt binarny lub obiekt bazy"""
    meme = MemesService.get_meme(meme_id=id, session=session)
    if not meme:
        raise HTTPException(status_code=404, detail=f"Meme with id={id} not found!")
    return FileResponse(str(meme.name), media_type="image/png")


@router.patch("/change_status")
def change_status(body: MemeSchema, session: Session = Depends(get_session)):
    """Do ewentualnego uzupełnienia - dowolna zmiana obiektu w bazie - mema"""
    with session as session:
        meme = session.query(Meme_db).filter_by(id=body.id).one_or_none()
        meme.status_id = body.status_id
        session.commit()
        session.flush()
    return 200


@router.get("/meme/{id}", status_code=200)
def get_file(id: str, session: Session = Depends(get_session)) -> FileResponse:
    """Zwróć mema jako obiekt binarny"""
    meme = MemesService.get_meme(meme_id=id, session=session)
    meme_filepath = meme.name
    return FileResponse(path=meme_filepath)


@router.patch("/like/{id}")
def add_like(id: str, session: Session = Depends(get_session)):
    """Dodaj polubienie do mema"""
    with session as session:
        meme = session.query(Meme_db).filter_by(id=id).one_or_none()
        meme.like += 1
        session.commit()
        session.flush()
    return 200


@router.delete("/delete/{id}")
def delete_meme(id: str, session: Session = Depends(get_session)):
    """Usuń mema jako obiekt z bazy i plik binarny z serwera wraz z katalogiem nadrzędnym"""
    with session as session:
        meme = session.query(Meme_db).filter_by(id=id).one_or_none()
        path_to_meme = Path(meme.name)
        parent_directory = path_to_meme.parent.absolute()
        shutil.rmtree(parent_directory)
        session.delete(meme)
        session.commit()
        session.flush()
    return 200


@router.patch("/accept/{id}")
def accept_meme(id: str, user: str, session: Session = Depends(get_session)):
    """Zaakceptuj wybranego mema"""
    with session as session:
        meme = session.query(Meme_db).filter_by(id=id).one_or_none()
        meme.status_id = 2
        meme.date_mod = datetime_now
        meme.accepted_by_user = user
        session.commit()
        session.flush()
    return 200
