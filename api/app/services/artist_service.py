# app/services/artist_service.py

from sqlalchemy.orm import Session
from app.models.artist import Artist as ArtistModel
from app.schemas import ArtistCreate


class ArtistService:
    def __init__(self, db: Session):
        self.db = db

    def create_artist(self, artist: ArtistCreate):
        db_artist = ArtistModel(name=artist.name)
        self.db.add(db_artist)
        self.db.commit()
        self.db.refresh(db_artist)
        return db_artist

    def get_artists(self, skip: int = 0, limit: int = 100):
        return self.db.query(ArtistModel).offset(skip).limit(limit).all()

    def get_artist(self, artist_id: int):
        return self.db.query(ArtistModel).filter(artist_id == ArtistModel.artist_id).first()

    def update_artist(self, artist_id: int, name: str):
        db_artist = self.db.query(ArtistModel).filter(artist_id == ArtistModel.artist_id).first()
        if db_artist:
            db_artist.name = name
            self.db.commit()
            self.db.refresh(db_artist)
        return db_artist

    def delete_artist(self, artist_id: int):
        db_artist = self.db.query(ArtistModel).filter(artist_id == ArtistModel.artist_id).first()
        if db_artist:
            self.db.delete(db_artist)
            self.db.commit()
            return True
        return False
