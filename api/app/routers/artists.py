from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import Artist as ArtistModel
from app.schemas import Artist, ArtistCreate
from app.repository import ArtistRepository
from app.database import get_db
from app.dependencies import get_current_active_user, get_current_active_admin

router = APIRouter()


@router.get("/", response_model=List[Artist], responses={
    200: {
        "description": "A list of artists"
    }
}, dependencies=[Depends(get_current_active_user)])
def read_artists(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    artists = ArtistRepository().get_all(db)
    return artists


@router.post("/", response_model=Artist, responses={
    200: {
        "description": "The newly created artist"
    }
}, dependencies=[Depends(get_current_active_admin)])
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = ArtistModel(name=artist.name)
    return ArtistRepository().create(db, db_artist)


@router.get("/{artist_id}", response_model=Artist, responses={
    200: {
        "description": "The artist with the specified ID"
    },
    404: {
        "description": "Artist not found"
    }
}, dependencies=[Depends(get_current_active_user)])
def read_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = ArtistRepository().get_by_id(db, artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.put("/{artist_id}", response_model=Artist, responses={
    200: {
        "description": "The updated artist"
    },
    404: {
        "description": "Artist not found"
    }
}, dependencies=[Depends(get_current_active_admin)])
def update_artist(artist_id: int, artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = ArtistRepository().get_by_id(db, artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    db_artist.name = artist.name
    return ArtistRepository().update(db, db_artist)


@router.delete("/{artist_id}", responses={
    200: {
        "description": "Artist deleted successfully"
    },
    404: {
        "description": "Artist not found"
    }
}, dependencies=[Depends(get_current_active_admin)])
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    db_artist = ArtistRepository().get_by_id(db, artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    ArtistRepository().delete(db, db_artist)
    return {"detail": "Artist deleted"}
