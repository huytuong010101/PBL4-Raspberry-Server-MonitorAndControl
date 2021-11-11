from pydantic import BaseModel, validator, EmailStr
from typing import Optional
from datetime import datetime
from utils.peewee_util import PeeweeGetterDict


class UserBase(BaseModel):
    username: str
    fullname: str
    avatar: Optional[str] = None
    email: Optional[EmailStr] = None
    is_admin: Optional[bool] = False

    @validator("username")
    def validate_username(cls, value: str):
        value = value.strip()
        if len(value) <= 4:
            raise ValueError("Length of username must greater then 4")
        return value

    @validator("fullname")
    def validate_fullname(cls, value: str):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Fullname is required")
        return value

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

    @validator("new_password")
    def password_validate(cls, value):
        if len(value) <= 4:
            raise ValueError("Length of password must greater then 4")
        return value

