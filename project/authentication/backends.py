
from datetime import datetime

from sqlalchemy.orm import Session
from jose import jwt

from main import settings
from .models import UserDbModel
from .schemas import UserResponseSchema

class AbstractUser():
    def __init__(self, db: Session, id: int = 0, email: str = None, password: str = None, token: str = None):
        self.db = db
        self.id = id
        self.email = email
        self.password = password
        self.token = token

    def _get_token(self):
        time_now = int(datetime.now().timestamp()) + settings.ACCESS_TOKEN_EXPIRE_SECONDS
        data = {
            "id"    : self.id,
            "time"  : time_now
        }

        token = jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)
        return token

    def _create_user(self):
        user = UserDbModel(email=self.email, password=self.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        self.id = user.id
        self.token = self._get_token()

        return AbstractUser(db=self.db, id=self.id, email=self.email, password=self.password, token=self.token)



class Authentication():
    def __init__(self, db: Session):
        self.db = db
    
    def registration(self, email: str, password: str):
        user = self.db.query(UserDbModel).filter(UserDbModel.email == email).first()
    
        if user:
            return UserResponseSchema(describtion="User exists in db!", status_code=400,  token=None)

        user = AbstractUser(db=self.db, email=email, password=password)._create_user()
        # token = user._get_token()
        return UserResponseSchema(describtion="Create new user!", status_code=201, token=user.token)
    
    def authentication(self, email: str, password: str):
        user = self.db.query(UserDbModel).filter(UserDbModel.email == email).first()
    
        if not user:
            return UserResponseSchema(describtion="User not exists!", status_code=401, token=None)

        if not (user.password == password):
            return UserResponseSchema(describtion="User not exists!", status_code=401, token=None)

        user = AbstractUser(db=self.db, id=user.id, email=email, password=password)
        token = user._get_token()
        return UserResponseSchema(describtion="Update user token!", status_code=202, token=token)

    def authorisation(self, token: str):
        try:
            data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        except Exception:
            return False

        user = self.db.query(UserDbModel).filter(UserDbModel.id == data['id']).first()

        if not user:
            return False

        if int(datetime.now().timestamp()) > data['time']:
            return False

        return True