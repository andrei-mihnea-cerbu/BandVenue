from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class FestivalDetail(Base):
    __tablename__ = 'festival_details'
    event_id = Column(Integer, ForeignKey('events.event_id'), primary_key=True)
    accommodation = Column(String)
    transport = Column(String)
    merchandise = Column(String)
    artist_payment = Column(Numeric(10, 2))

    event = relationship("Event", back_populates="festival_detail")
