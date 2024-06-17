from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ConcertDetail(Base):
    __tablename__ = 'concert_details'
    event_id = Column(Integer, ForeignKey('events.event_id'), primary_key=True)
    accommodation = Column(String)
    transport = Column(String)
    ticket_price = Column(Numeric(10, 2))
    physical_tickets = Column(Integer)
    electronic_tickets = Column(Integer)
    electronic_ticket_fee = Column(Numeric(10, 2))
    culture_tax = Column(Numeric(10, 2))

    event = relationship("Event", back_populates="concert_detail")
