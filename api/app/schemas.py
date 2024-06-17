from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: str = "User"


class User(UserBase):
    user_id: int
    role: str
    suspended_account: bool

    class Config:
        from_attributes = True


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr
    new_password: str


class ArtistBase(BaseModel):
    name: str


class ArtistCreate(ArtistBase):
    user_id: int


class Artist(ArtistBase):
    artist_id: int
    user: User

    class Config:
        from_attributes = True


class FestivalDetailBase(BaseModel):
    accommodation: Optional[str]
    transport: Optional[str]
    merchandise: Optional[str]
    artist_payment: Optional[float]


class FestivalDetailCreate(FestivalDetailBase):
    pass


class FestivalDetail(FestivalDetailBase):
    event_id: int

    class Config:
        from_attributes = True


class ConcertDetailBase(BaseModel):
    accommodation: Optional[str]
    transport: Optional[str]
    ticket_price: Optional[float]
    physical_tickets: Optional[int]
    electronic_tickets: Optional[int]
    electronic_ticket_fee: Optional[float]
    culture_tax: Optional[float]


class ConcertDetailCreate(ConcertDetailBase):
    pass


class ConcertDetail(ConcertDetailBase):
    event_id: int

    class Config:
        from_attributes = True


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
