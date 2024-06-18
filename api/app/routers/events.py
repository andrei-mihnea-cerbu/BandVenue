from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import Response

from app.schemas import Event, EventCreate
from app.database import get_db
from app.services.event_service import create_event, get_events, get_event, update_event, delete_event
from app.dependencies import get_current_active_user

router = APIRouter()


@router.post("/",
             response_model=Event,
             status_code=status.HTTP_201_CREATED,
             responses={
                 201: {
                     "description": "The newly created event with its details",
                     "content": {
                         "application/json": {
                             "example": {
                                 "event_id": 1,
                                 "artist_id": 1,
                                 "name": "Rock Festival",
                                 "date": "2024-06-20",
                                 "location": "New York",
                                 "event_type": "Festival",
                                 "festival_detail": {
                                     "accommodation": "Hotel",
                                     "transport": "Bus",
                                     "merchandise": "T-Shirts",
                                     "artist_payment": 5000.00
                                 },
                                 "concert_detail": None
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
def create_event_handler(event: EventCreate, db: Session = Depends(get_db)):
    """
    Creates a new event record. Accessible to authenticated users.
    """
    return create_event(event, db)


@router.get("/",
            response_model=List[Event],
            responses={
                200: {
                    "description": "A list of events",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "event_id": 1,
                                    "artist_id": 1,
                                    "name": "Rock Festival",
                                    "date": "2024-06-20",
                                    "location": "New York",
                                    "event_type": "Festival",
                                    "festival_detail": {
                                        "accommodation": "Hotel",
                                        "transport": "Bus",
                                        "merchandise": "T-Shirts",
                                        "artist_payment": 5000.00
                                    },
                                    "concert_detail": None
                                },
                                {
                                    "event_id": 2,
                                    "artist_id": 2,
                                    "name": "Jazz Concert",
                                    "date": "2024-07-15",
                                    "location": "Chicago",
                                    "event_type": "Personal Concert",
                                    "festival_detail": None,
                                    "concert_detail": {
                                        "accommodation": "Airbnb",
                                        "transport": "Plane",
                                        "ticket_price": 75.00,
                                        "physical_tickets": 100,
                                        "electronic_tickets": 200,
                                        "electronic_ticket_fee": 5.00,
                                        "culture_tax": 2.00
                                    }
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
def read_events_handler(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of events. Accessible to any authenticated user.
    """
    return get_events(skip, limit, db)


@router.get("/{event_id}",
            response_model=Event,
            responses={
                200: {
                    "description": "The event with the specified ID",
                    "content": {
                        "application/json": {
                            "example": {
                                "event_id": 1,
                                "artist_id": 1,
                                "name": "Rock Festival",
                                "date": "2024-06-20",
                                "location": "New York",
                                "event_type": "Festival",
                                "festival_detail": {
                                    "accommodation": "Hotel",
                                    "transport": "Bus",
                                    "merchandise": "T-Shirts",
                                    "artist_payment": 5000.00
                                },
                                "concert_detail": None
                            }
                        }
                    }
                },
                404: {
                    "description": "Event not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Event not found"
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
def read_event_handler(event_id: int, db: Session = Depends(get_db)):
    """
    Retrieves specific event details. Accessible to any authenticated user.
    """
    event = get_event(event_id, db)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            responses={
                204: {
                    "description": "Event updated successfully",
                    "content": {}
                },
                404: {
                    "description": "Event not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Event not found"
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
def update_event_handler(event_id: int, event: EventCreate, db: Session = Depends(get_db)):
    """
    Updates an event's details. Only accessible to authenticated users.
    """
    updated_event = update_event(event_id, event, db)
    if updated_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{event_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               responses={
                   204: {
                       "description": "Event deleted successfully",
                       "content": {}
                   },
                   404: {
                       "description": "Event not found",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Event not found"
                               }
                           }
                       }
                   }
               },
               dependencies=[Depends(get_current_active_user)])
def delete_event_handler(event_id: int, db: Session = Depends(get_db)):
    """
    Deletes an event record. Only accessible to authenticated users.
    """
    deleted_event = delete_event(event_id, db)
    if deleted_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
