from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import Response

from app.schemas import Artist, ArtistCreate
from app.database import get_db
from app.schemas.artist import ArtistBase
from app.services import artist_service_class
from app.dependencies import authenticate_user

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
             dependencies=[Depends(authenticate_user)])
def create_artist_handler(artist: ArtistCreate):
    """
    Creates a new artist record. Accessible to authenticated users.
    """
    return artist_service_class.create_artist(artist)


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
            })
def read_artists_handler(skip: int = 0, limit: int = 10):
    """
    Retrieves a list of artists. Accessible to any authenticated user.
    """
    return artist_service_class.get_artists(skip, limit)


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
            })
def read_artist_handler(artist_id: int):
    """
    Retrieves specific artist details. Accessible to any authenticated user.
    """
    artist = artist_service_class.get_artist(artist_id)
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
            })
def update_artist_handler(artist_id: int, artist: ArtistBase):
    """
    Updates an artist's details. Only accessible to authenticated users.
    """
    updated_artist = artist_service_class.update_artist(artist_id, artist.name)
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
               })
def delete_artist_handler(artist_id: int):
    """
    Deletes an artist record. Only accessible to authenticated users.
    """
    deleted_artist = artist_service_class.delete_artist(artist_id)
    if deleted_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
