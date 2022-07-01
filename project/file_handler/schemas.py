
from datetime import datetime

from pydantic import BaseModel, validator

from fastapi import UploadFile, File


class Photo(BaseModel):
    name: str = "file_name"
    date: datetime = datetime.now()


class PhotoExtand(Photo):
    img: str = 'url://.../.../..'


class RequestPostPhotoSchema(BaseModel):
    token: str
    photos: list[UploadFile] = File(...)

    @validator('photos')
    def chek_count_of_files(cls, photos: list[UploadFile]):
        if len(photos) > 15:
            raise ValueError('ValueError: More photos uploads. You can send 15 photos maximum!')
        return photos

    @validator('photos')
    def check_type_of_files(cls, photos: list[UploadFile]):
        for photo in photos:
            if photo.content_type != 'image/jpeg':
                raise ValueError('ValueError: The send file[s] is not .jpeg format. You can send only .jpeg format files!')
        return photos

    class Config:
        orm_mode = True


class ResponsePostPhotoSchema(BaseModel):
    describtion: str = None
    status_code: int = None
    code: str = None
    data: list[Photo] = File(...)


class RequestGetDeletePhotoSchema(BaseModel):
    token: str
    code: str

    @validator('code')
    def check_correct_code(cls, code: str):
        if len(code) != 32:
            raise ValueError('ValueError: The send of your code is not valid!')
        return code

    class Config:
        orm_mode = True


class ResponseGetPhotoSchema(ResponsePostPhotoSchema):
    data: list[PhotoExtand] = File(...)


class ResponseDeletePhotoSchema(BaseModel):
    describtion: str = None
    status_code: int = None