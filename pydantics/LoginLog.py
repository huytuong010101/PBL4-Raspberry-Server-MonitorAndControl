from pydantic import BaseModel
from typing import Optional
from utils.peewee_util import PeeweeGetterDict
from datetime import datetime


class BriefUser(BaseModel):
    username: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class LoginLogOut(BaseModel):
    time: datetime
    device: Optional[str]
    user: BriefUser

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
