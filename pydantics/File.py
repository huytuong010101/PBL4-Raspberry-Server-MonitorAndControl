from pydantic import BaseModel
from datetime import datetime


class FileOut(BaseModel):
    name: str
    type: str = None
    size: int = None
    modified_at: datetime = None
    created_at: datetime = None


class FileUpdate(BaseModel):
    name: str
    path: str


class DirIn(BaseModel):
    base_path: str
    dir_name: str


