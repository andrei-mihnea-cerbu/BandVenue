from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    suspended_account = Column(Boolean, default=False)
    role = Column(Enum('User', 'Admin', name='user_roles'), nullable=False, server_default='User')

    artists = relationship("Artist", back_populates="user")

class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship("User", back_populates="artists")
    events = relationship("Event", back_populates="artist")

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

class FestivalDetail(Base):
    __tablename__ = 'festival_details'
    event_id = Column(Integer, ForeignKey('events.event_id'), primary_key=True)
    accommodation = Column(String)
    transport = Column(String)
    merchandise = Column(String)
    artist_payment = Column(Numeric(10, 2))

    event = relationship("Event", back_populates="festival_detail")

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
