from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from utils.peewee_util import PeeweeGetterDict


class UserBase(BaseModel):
    username: str
    fullname: str
    avatar: Optional[str] = None
    email: Optional[str] = None
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserOut(UserBase):
    created_at: datetime
    created_by: Optional[UserBase] = None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserIn(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class Password(BaseModel):
    old_password: Optional[str] = None
    new_password: str

