from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    on_duty = Column(String)
    role = Column(String)
    card_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    # One-to-one relationship with IDCard
    id_card = relationship("IDCard", back_populates="user", uselist=False)  # uselist=False means only one card per user
class IDCard(Base):
    __tablename__ = 'id_cards'
    id = Column(Integer, primary_key=True,index=True)
    card_number = Column(Integer, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    issue_date = Column(String)
    expiration_date = Column(String)
    status = Column(String)  # e.g., 'active', 'inactive', 'lost'
    issue_location = Column(String)  # e.g., 'New York', 'Los Angeles'
        # Back-reference to User
    user = relationship("User", back_populates="id_card")