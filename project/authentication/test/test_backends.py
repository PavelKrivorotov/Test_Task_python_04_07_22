
from jose import jwt
from jose.exceptions import JWTError
import pytest

from manage import SessionLocal_test
from main import settings
from authentication.models import UserDbModel
from authentication.schemas import UserResponseSchema
from authentication.backends import AbstractUser, Authentication


class TestAbstractUser():
    @pytest.fixture(scope='function')
    def db_connect(self):
        db = SessionLocal_test()

        yield db

        db.query(UserDbModel).delete()
        db.commit()
        db.close()

    def test_abstract_user(self, db_connect):
        check = AbstractUser(db=db_connect, id=1, email='pavel@mail.ru', password='1234', token='Your token')
        expect = {'db' : db_connect, 'id' : 1, 'email' : 'pavel@mail.ru', 'password' : '1234', 'token' : 'Your token'}

        assert expect == check.__dict__, 'Not correct parametrs of AbstractUser class!'

    def test_get_token(self, db_connect):
        user = AbstractUser(db=db_connect, id=1, email='pavel@mail.ru', password='1234')

        token = user._get_token()

        try:
            data = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except Exception:
            assert 1 == 0, 'Not correct jwt-token!'

        assert data['id'] == 1, 'Not correct jwt-token!'

    def test_create_user(self, db_connect):
        user = AbstractUser(db=db_connect, id=1, email='pavel@mail.ru', password='1234')._create_user()
        expect = user.db.query(UserDbModel).filter(UserDbModel.id == 1).first()

        assert expect is not None, 'Not correct new user in db!'


class TestAuthentication():
    @pytest.fixture(scope='function')
    def db_connect(self):
        db = SessionLocal_test()

        yield db

        db.query(UserDbModel).delete()
        db.commit()
        db.close()

    def test_authentication(self, db_connect):
        check = Authentication(db=db_connect)
        expect = {'db' : db_connect}

        assert expect == check.__dict__

    def test_registration_method_1(self, db_connect):
        user = AbstractUser(db=db_connect, email='pavel@mail.ru', password='1234')._create_user()
        check = Authentication(db=db_connect).registration(email=user.email, password=user.password)
        expect = UserResponseSchema(describtion='User exists in db!', status_code=400, token=None)

        assert expect == check, 'Not correct registration exists user!'

    def test_registration_method_2(self, db_connect):
        user = AbstractUser(db=db_connect, email='vika@mail.ru', password='123')
        check = Authentication(db=db_connect).registration(email=user.email, password=user.password)
        expect = UserResponseSchema(describtion="Create new user!", status_code=201, token=check.token)

        assert expect == check , 'Not correct registration new user!'

    def test_authentication_method_1(self, db_connect):
        user = AbstractUser(db=db_connect, email='pavel@mail.ru', password='1234')._create_user()
        check = Authentication(db=db_connect).authentication(email=user.email, password=user.password)
        expect = UserResponseSchema(describtion="Update user token!", status_code=202, token=check.token)

        assert expect == check, 'Not correct about created user can not update self token!'

    def test_authentication_method_2(self, db_connect):
        user = AbstractUser(db=db_connect, email='pavel@mail.ru', password='123')
        check = Authentication(db=db_connect).authentication(email=user.email, password=user.password)
        expect = UserResponseSchema(describtion="User not exists!", status_code=401, token=None)

        assert expect == check, 'Not correct email and password data!'

    def test_authentication_method_3(self, db_connect):
        user = AbstractUser(db=db_connect, email='vika@mail.ru', password='123')
        check = Authentication(db=db_connect).authentication(email=user.email, password=user.password)
        expect = UserResponseSchema(describtion="User not exists!", status_code=401, token=None)

        assert expect == check, 'Not correct email and password data!'

    def test_authorisation_method_1(self, db_connect):
        user = AbstractUser(db=db_connect, email='pavel@mail.ru', password='1234')._create_user()
        expect = Authentication(db=db_connect).authorisation(token=user.token)

        assert expect == True

    def test_authorisation_method_2(self, db_connect):
        expect = Authentication(db=db_connect).authorisation(token='Not valid token')

        assert expect == False

    def test_authorisation_method_3(self, db_connect):
        pass

    def test_authorisation_method_4(self, db_connect):
        pass