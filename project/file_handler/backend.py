
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from fastapi import UploadFile

from main import settings

from .models import PhotoDbModel
from .schemas import Photo, PhotoExtand, ResponseDeletePhotoSchema, ResponsePostPhotoSchema, ResponseGetPhotoSchema


class AbstractPhotos():
    def __init__(self, db: Session):
        self.db = db

    def _get_bucket_name(self, date = datetime.now()):
        bucket = settings.CLIENT.Bucket(date.strftime("%Y%m%d"))

        if not (bucket in settings.CLIENT.buckets.all()):
            bucket.create()

        return bucket

    def _get_code_photos(self):
        return uuid4().hex

    def _save_photo(self, photo: UploadFile, photo_name: str, bucket):
        bucket.upload_fileobj(photo.file, photo_name)

    def _destroy_photo(self, photo_name: str, bucket):
        bucket.delete_objects(Delete={'Objects': [{"Key" : photo_name}]})
    
    def add_photos(self, photos: list[UploadFile]):
        bucket = self._get_bucket_name()
        photos_code = self._get_code_photos()
        data = []

        for photo in photos:
            photo_name = f'{uuid4().hex}.jpeg'

            obj_1 = PhotoDbModel(code=photos_code, name=photo_name)
            self.db.add(obj_1)

            self._save_photo(photo=photo, photo_name=photo_name, bucket=bucket)

            obj_2 = Photo(name=photo_name)
            data.append(obj_2)
    
        self.db.commit()
        return ResponsePostPhotoSchema(describtion="Added photos on server!", status_code=202, code=photos_code, data=data)

    def get_photos(self, code: str):
        photos = self.db.query(PhotoDbModel).filter(PhotoDbModel.code == code).all()
        data = []

        if not photos:
            return ResponseGetPhotoSchema(describtion="Photos is not detected!", status_code=204, code=code, data=data)

        for photo in photos:
            img = f'http://localhost:9000/photos/{photo.date.strftime("%Y%m%d")}/{photo.name}'

            obj_1 = PhotoExtand(name=photo.name, date=photo.date, img = img)
            data.append(obj_1)
        
        return ResponseGetPhotoSchema(describtion="Photos for your code", status_code=200, code=code, data=data)

    def delete_photos(self, code: str):
        photos = self.db.query(PhotoDbModel).filter(PhotoDbModel.code == code).all()

        if not photos:
            return ResponseDeletePhotoSchema(describtion='Files is not detected!', status_code=204)

        for photo in photos:
            bucket = self._get_bucket_name(photo.date)
            # bucket.delete_objects(Delete={'Objects': [{"Key" : photo.name}]})
            self._destroy_photo(photo_name=photo.name, bucket=bucket)

        self.db.query(PhotoDbModel).filter(PhotoDbModel.code == code).delete(synchronize_session='evaluate')
        self.db.commit()

        return ResponseDeletePhotoSchema(describtion='Files deleted!', status_code=200)
