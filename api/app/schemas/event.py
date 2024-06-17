from pydantic import BaseModel
from typing import Optional
from datetime import date
from .artist import Artist
from .festival_detail import FestivalDetail, FestivalDetailCreate
from .concert_detail import ConcertDetail, ConcertDetailCreate


class EventBase(BaseModel):
    name: str
    date: date
    location: str
    event_type: str


class EventCreate(EventBase):
    artist_id: int
    festival_detail: Optional[FestivalDetailCreate]
    concert_detail: Optional[ConcertDetailCreate]


class Event(EventBase):
    event_id: int
    artist: Optional[Artist]
    festival_detail: Optional[FestivalDetail]
    concert_detail: Optional[ConcertDetail]

    class Config:
        from_attributes = True
