from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    event_type = Column(Enum("Festival", "Personal Concert", name="event_type"), nullable=False)

    artist = relationship("Artist", back_populates="events")
    festival_detail = relationship("FestivalDetail", uselist=False, back_populates="event")
    concert_detail = relationship("ConcertDetail", uselist=False, back_populates="event")
