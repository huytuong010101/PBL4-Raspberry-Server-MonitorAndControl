from pydantic import BaseModel


class AppOut(BaseModel):
    name: str
