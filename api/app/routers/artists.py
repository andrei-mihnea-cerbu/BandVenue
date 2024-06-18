# app/routers/artists.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import Response

from app.schemas import Artist, ArtistCreate
from app.database import get_db
from app.services.artist_service import create_artist, get_artists, get_artist, update_artist, delete_artist
from app.dependencies import get_current_active_user

router = APIRouter()


@router.post("/", response_model=Artist, status_code=status.HTTP_201_CREATED, responses={
    201: {
        "description": "The newly created artist",
        "content": {
            "application/json": {
                "example": {
                    "artist_id": 1,
                    "name": "Artist1"
                }
            }
        }
    },
    400: {
        "description": "Invalid input"
    }
}, dependencies=[Depends(get_current_active_user)])
def create_artist_handler(artist: ArtistCreate, db: Session = Depends(get_db)):
    return create_artist(artist, db)


@router.get("/", response_model=List[Artist], responses={
    200: {
        "description": "A list of artists"
    }
}, dependencies=[Depends(get_current_active_user)])
def read_artists_handler(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_artists(skip, limit, db)


@router.get("/{artist_id}", response_model=Artist, responses={
    200: {
        "description": "The artist with the specified ID"
    },
    404: {
        "description": "Artist not found"
    }
}, dependencies=[Depends(get_current_active_user)])
def read_artist_handler(artist_id: int, db: Session = Depends(get_db)):
    artist = get_artist(artist_id, db)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.put("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_artist_handler(artist_id: int, artist: ArtistCreate, db: Session = Depends(get_db)):
    update_artist(artist_id, artist, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artist_handler(artist_id: int, db: Session = Depends(get_db)):
    delete_artist(artist_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
