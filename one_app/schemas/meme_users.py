from pydantic import BaseModel

from one_app.schemas.meme_enums import RoleEnum


class Role(BaseModel):
    id: int
    name: RoleEnum

    class Config:
        orm_mode = True
        use_enum_values = True


class User(BaseModel):
    id: int
    nick: str
    email: str
    user_role: Role = RoleEnum.user

    class Config:
        orm_mode = True
        use_enum_values = True
