
from fastapi import Depends, FastAPI

from sqlalchemy.orm import Session

from authentication.schemas import UserRequestSchema, UserResponseSchema
from authentication.backends import NewAuthentication
from file_handler.schemas import (
    RequestPostPhotoSchema, RequestGetDeletePhotoSchema, ResponsePostPhotoSchema,
    ResponseGetPhotoSchema, ResponseDeletePhotoSchema)
from file_handler.backend import AbstractPhotos
from main.settings import Base, SessionLocal, engine, test_SessionLocal, test_engine


Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=test_engine)
# print(Base.metadata.tables)
# print(type(Base.metadata.tables['users'].c))

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_test():
    db = test_SessionLocal()
    try:
        yield db
    except:
        db.close()

@app.post("/users/registration/", response_model=UserResponseSchema)
def registartion(user_schema: UserRequestSchema = Depends(), db: Session = Depends(get_db)):
    resp = NewAuthentication(db=db)
    resp = resp.registartion(email=user_schema.email, password=user_schema.password)

    return resp


@app.post("/users/authorization/", response_model=UserResponseSchema)
def authorisation(user_schema: UserRequestSchema = Depends(), db: Session = Depends(get_db)):
    resp = NewAuthentication(db=db)
    resp = resp.authentication(email=user_schema.email, password=user_schema.password)

    return resp


@app.post("/frames/", response_model=ResponsePostPhotoSchema)
def add_photos(files: RequestPostPhotoSchema = Depends(), db: Session = Depends(get_db)):
    if not NewAuthentication(db=db).authorisation(token=files.dict()['token']):
        return ResponsePostPhotoSchema(describtion="No authorisate!", status_code=401 ,data=[])

    resp = AbstractPhotos(db=db)
    resp = resp.add_photos(files.dict()['photos'])

    return resp


@app.get("/frames/", response_model=ResponseGetPhotoSchema)
def get_photos(req: RequestGetDeletePhotoSchema = Depends(), db: Session = Depends(get_db)):
    if not NewAuthentication(db=db).authorisation(token=req.dict()['token']):
        return ResponseGetPhotoSchema(describtion="No authorisate!", status_code=401, data=[])

    resp = AbstractPhotos(db=db)
    resp = resp.get_photos(code=req.code)

    return resp


@app.delete("/frames/", response_model=ResponseDeletePhotoSchema)
def delete_photos(req: RequestGetDeletePhotoSchema = Depends(), db: Session = Depends(get_db)):
    if not NewAuthentication(db=db).authorisation(token=req.dict()['token']):
        return ResponseDeletePhotoSchema(describtion="No authorisate!", status_code=401)

    resp = AbstractPhotos(db=db)
    resp = resp.delete_photos(req.code)

    return resp