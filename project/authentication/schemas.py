
from typing import Union

from pydantic import BaseModel


class UserRequestSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserResponseSchema(BaseModel):
    describtion: Union[str, None] = None
    status_code: Union[int, None] = None
    token: Union[str, None] = None

    class Config:
        orm_mode = True