from pydantic import BaseModel
from typing import Optional
from utils.peewee_util import PeeweeGetterDict
from datetime import datetime


class ResourceOut(BaseModel):
    time: datetime
    ram_percent: Optional[float]
    cpu_percent: Optional[float]
    temperature_percent: Optional[float]
    network_send: Optional[float]
    network_receive: Optional[float]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
