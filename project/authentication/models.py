
from sqlalchemy import Column, Integer
from sqlalchemy_utils import EmailType, PasswordType

from main.settings import Base


class UserDbModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType)
    password = Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt']))