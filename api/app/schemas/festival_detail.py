from pydantic import BaseModel
from typing import Optional


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
