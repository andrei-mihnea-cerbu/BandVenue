from pydantic import BaseModel
from typing import Optional


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
