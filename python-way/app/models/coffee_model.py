from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime,Float
from datetime import datetime


class Coffee(Base):
    __tablename__ = 'coffee'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    introduced =Column(DateTime, default=datetime.now())
    image_url = Column(String) 