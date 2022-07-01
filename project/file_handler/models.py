
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from main.settings import Base


class PhotoDbModel(Base):
    __tablename__ = "inbox"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    name = Column(String)
    date = Column(DateTime, default=datetime.now())