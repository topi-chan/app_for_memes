import uuid

from datetime import datetime
from pytz import timezone
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base
from one_app.schemas.meme_enums import MemeStatusEnum, RoleEnum

UTC = timezone('UTC')


def time_now():
    return datetime.now(UTC)


class Role(Base):

    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(RoleEnum))


class User(Base):

    __tablename__ = "domain_user"

    id = Column(Integer, primary_key=True)
    nick = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    user_role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    user_role = relationship("Role")


class Status(Base):

    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(MemeStatusEnum))


class Meme(Base):

    __tablename__ = "meme"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid ()"),
    )
    name = Column(String, nullable=True, unique=False)
    like = Column(Integer, nullable=False, unique=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    date_add = Column(DateTime, nullable=False, unique=False, default=time_now)
    date_mod = Column(DateTime, nullable=True, unique=False)
    nick = Column(String, nullable=False, unique=False)
    description = Column(String, nullable=True, unique=False)
    best = Column(Boolean, nullable=False, unique=False, default=False)
    alias = Column(String, nullable=False, unique=True)
    width = Column(Integer, nullable=False, unique=False)
    height = Column(Integer, nullable=False, unique=False)
    accepted_by_user = Column(String, nullable=True, unique=False)
    meme_status = relationship("Status")
