from pydantic import BaseModel
from typing import Optional
from .user import User


class ArtistBase(BaseModel):
    name: str


class ArtistCreate(ArtistBase):
    user_id: int


class Artist(ArtistBase):
    artist_id: int
    user: Optional[User]

    class Config:
        from_attributes = True
