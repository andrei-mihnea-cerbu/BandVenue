from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship("User", back_populates="artists")
    events = relationship("Event", back_populates="artist")
