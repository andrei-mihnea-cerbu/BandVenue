from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import Response

from app.schemas import Event, EventCreate
from app.database import get_db
from app.services import event_service_class

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
             })
def create_event_handler(event: EventCreate):
    """
    Creates a new event record. Accessible to authenticated users.
    """
    return event_service_class.create_event(event)


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
            })
def read_events_handler(skip: int = 0, limit: int = 10):
    """
    Retrieves a list of events. Accessible to any authenticated user.
    """
    return event_service_class.get_events(skip, limit)


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
            })
def read_event_handler(event_id: int):
    """
    Retrieves specific event details. Accessible to any authenticated user.
    """
    event = event_service_class.get_event(event_id)
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
            })
def update_event_handler(event_id: int, event: EventCreate):
    """
    Updates an event's details. Only accessible to authenticated users.
    """
    updated_event = event_service_class.update_event(event_id, event)
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
               })
def delete_event_handler(event_id: int):
    """
    Deletes an event record. Only accessible to authenticated users.
    """
    deleted_event = event_service_class.delete_event(event_id)
    if deleted_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
