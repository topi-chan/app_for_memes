import typing as t
from datetime import datetime
from uuid import UUID

from one_app.db.meme_models import Meme, Status
from pytz import timezone
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

UTC = timezone("UTC")
datetime_now = datetime.now(UTC)


def split_memes(memes, items_per_page):
    splitted_memes = [
        memes[x: x + items_per_page] for x in range(0, len(memes), items_per_page)
    ]
    return splitted_memes


class MemesService:
    @staticmethod
    def get_memes(*, session: Session) -> t.Iterator[Meme]:
        return session.query(Meme).all()

    @staticmethod
    def get_memes_by_date(*, session: Session) -> t.Iterator[Meme]:
        result = session.query(Meme).where(Meme.status_id == 2).order_by(desc(Meme.date_mod)).all()
        return result

    @staticmethod
    def get_memes_by_like(*, session: Session) -> t.Iterator[Meme]:
        result = session.query(Meme).where(Meme.status_id == 2).order_by(desc(Meme.like)).all()
        return result

    @staticmethod
    def get_best_memes(*, session: Session) -> t.Iterator[Meme]:
        result = session.query(Meme).where(Meme.best == True).order_by(desc(Meme.date_mod)).all()
        return result

    @staticmethod
    def get_accepted_memes(*, session: Session) -> t.Iterator[Meme]:
        accepted_memes_query_result = session.execute(
            select(Meme).where(Meme.status_id == 2)
        )
        accepted_memes = [meme for meme, in accepted_memes_query_result]
        return accepted_memes

    @staticmethod
    def get_meme(*, meme_id: UUID, session: Session) -> Meme:
        return session.query(Meme).filter(Meme.id == meme_id).one_or_none()

    @staticmethod
    def create_meme(
        *,
        name: str,
        like: int,
        status_id: int,
        date_add: datetime_now,
        date_mod: datetime,
        nick: str,
        alias: str,
        width: int,
        height: int,
        description: str,
        best: bool,
        session: Session,
    ) -> Meme:

        status = session.query(Status).filter(Status.id == status_id).first()
        meme = Meme(
            name=name,
            like=like,
            status_id=status.id,
            date_add=date_add,
            date_mod=date_mod,
            nick=nick,
            alias=alias,
            width=width,
            height=height,
            description=description,
            best=best,
        )

        session.add(meme)
        session.commit()
        session.flush()
        session.refresh(meme)

        return meme
