from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import Response

from app.schemas import Artist, ArtistCreate
from app.database import get_db
from app.services.artist_service import create_artist, get_artists, get_artist, update_artist, delete_artist
from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=Artist,
             status_code=status.HTTP_201_CREATED,
             responses={
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
                     "description": "Invalid input",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid input provided"
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             },
             dependencies=[Depends(get_current_active_user)])
def create_artist_handler(artist: ArtistCreate, db: Session = Depends(get_db)):
    """
    Creates a new artist record. Accessible to authenticated users.
    """
    return create_artist(artist, db)


@router.get("/",
            response_model=List[Artist],
            responses={
                200: {
                    "description": "A list of artists",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "artist_id": 1,
                                    "name": "Artist1"
                                },
                                {
                                    "artist_id": 2,
                                    "name": "Artist2"
                                }
                            ]
                        }
                    }
                },
                422: {
                    "description": "Invalid data.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Invalid query parameters"
                            }
                        }
                    }
                }
            },
            dependencies=[Depends(get_current_active_user)])
def read_artists_handler(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of artists. Accessible to any authenticated user.
    """
    return get_artists(skip, limit, db)


@router.get("/{artist_id}",
            response_model=Artist,
            responses={
                200: {
                    "description": "The artist with the specified ID",
                    "content": {
                        "application/json": {
                            "example": {
                                "artist_id": 1,
                                "name": "Artist1"
                            }
                        }
                    }
                },
                404: {
                    "description": "Artist not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Artist not found"
                            }
                        }
                    }
                },
                422: {
                    "description": "Invalid data.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Invalid path parameter"
                            }
                        }
                    }
                }
            },
            dependencies=[Depends(get_current_active_user)])
def read_artist_handler(artist_id: int, db: Session = Depends(get_db)):
    """
    Retrieves specific artist details. Accessible to any authenticated user.
    """
    artist = get_artist(artist_id, db)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.put("/{artist_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            responses={
                204: {
                    "description": "Artist updated successfully",
                    "content": {}
                },
                404: {
                    "description": "Artist not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Artist not found"
                            }
                        }
                    }
                },
                422: {
                    "description": "Invalid data.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Invalid body format"
                            }
                        }
                    }
                }
            },
            dependencies=[Depends(get_current_active_user)])
def update_artist_handler(artist_id: int, artist: ArtistCreate, db: Session = Depends(get_db)):
    """
    Updates an artist's details. Only accessible to authenticated users.
    """
    updated_artist = update_artist(artist_id, artist.name, db)
    if updated_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{artist_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               responses={
                   204: {
                       "description": "Artist deleted successfully",
                       "content": {}
                   },
                   404: {
                       "description": "Artist not found",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Artist not found"
                               }
                           }
                       }
                   }
               },
               dependencies=[Depends(get_current_active_user)])
def delete_artist_handler(artist_id: int, db: Session = Depends(get_db)):
    """
    Deletes an artist record. Only accessible to authenticated users.
    """
    deleted_artist = delete_artist(artist_id, db)
    if deleted_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
