from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from one_app.schemas.meme_enums import MemeStatusEnum


class Status(BaseModel):
    id: int
    name: MemeStatusEnum

    class Config:
        orm_mode = True
        use_enum_values = True


class Meme(BaseModel):
    id: UUID
    name: Optional[str] = None
    like: int
    status_id: int
    date_add: datetime
    date_mod: Optional[datetime] = None
    nick: str
    alias: str
    width: int
    height: int
    description: Optional[str] = None
    best: bool
    accepted_by_user: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class MemeCreate(BaseModel):
    meme_id: UUID
    name: Optional[str] = None
    like: int = 0
    status_id: int = 1
