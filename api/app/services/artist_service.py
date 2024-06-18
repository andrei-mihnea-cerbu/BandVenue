# app/services/artist_service.py
from sqlalchemy.orm import Session
from app.models import Artist as ArtistModel
from app.schemas import ArtistCreate


def create_artist(artist: ArtistCreate, db: Session):
    db_artist = ArtistModel(name=artist.name)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


def get_artists(skip: int = 0, limit: int = 100, db: Session = None):
    return db.query(ArtistModel).offset(skip).limit(limit).all()


def get_artist(artist_id: int, db: Session):
    return db.query(ArtistModel).filter(artist_id == ArtistModel.artist_id).first()


def update_artist(artist_id: int, name: str, db: Session):
    db_artist = db.query(ArtistModel).filter(artist_id == ArtistModel.artist_id).first()
    if db_artist:
        db_artist.name = name
        db.commit()
    return db_artist


def delete_artist(artist_id: int, db: Session):
    db_artist = db.query(ArtistModel).filter(artist_id == ArtistModel.artist_id).first()
    if db_artist:
        db.delete(db_artist)
        db.commit()
