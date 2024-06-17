from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    suspended_account = Column(Boolean, default=False)
    role = Column(Enum('User', 'Admin', name='user_roles'), nullable=False, server_default='User')

    artists = relationship("Artist", back_populates="user")
