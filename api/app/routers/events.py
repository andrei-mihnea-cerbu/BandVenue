from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import Event as EventModel, FestivalDetail as FestivalDetailModel, ConcertDetail as ConcertDetailModel
from app.schemas import Event, EventCreate
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter()


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED, responses={
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
        "description": "Invalid input"
    }
}, dependencies=[Depends(get_current_active_user)])
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = EventModel(
        artist_id=event.artist_id,
        name=event.name,
        date=event.date,
        location=event.location,
        event_type=event.event_type
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    if event.event_type == "Festival" and event.festival_detail:
        db_festival_detail = FestivalDetailModel(
            event_id=db_event.event_id,
            accommodation=event.festival_detail.accommodation,
            transport=event.festival_detail.transport,
            merchandise=event.festival_detail.merchandise,
            artist_payment=event.festival_detail.artist_payment
        )
        db.add(db_festival_detail)
        db.commit()
        db.refresh(db_festival_detail)

    if event.event_type == "Personal Concert" and event.concert_detail:
        db_concert_detail = ConcertDetailModel(
            event_id=db_event.event_id,
            accommodation=event.concert_detail.accommodation,
            transport=event.concert_detail.transport,
            ticket_price=event.concert_detail.ticket_price,
            physical_tickets=event.concert_detail.physical_tickets,
            electronic_tickets=event.concert_detail.electronic_tickets,
            electronic_ticket_fee=event.concert_detail.electronic_ticket_fee,
            culture_tax=event.concert_detail.culture_tax
        )
        db.add(db_concert_detail)
        db.commit()
        db.refresh(db_concert_detail)

    return db_event


@router.get("/", response_model=List[Event], responses={
    200: {
        "description": "A list of events"
    }
}, dependencies=[Depends(get_current_active_user)])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(EventModel).offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=Event, responses={
    200: {
        "description": "The event with the specified ID"
    },
    404: {
        "description": "Event not found"
    }
}, dependencies=[Depends(get_current_active_user)])
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=Event, responses={
    200: {
        "description": "The updated event"
    },
    404: {
        "description": "Event not found"
    }
}, dependencies=[Depends(get_current_active_user)])
def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    db_event.name = event.name
    db_event.date = event.date
    db_event.location = event.location
    db_event.event_type = event.event_type

    if event.event_type == "Festival" and event.festival_detail:
        db_festival_detail = db.query(FestivalDetailModel).filter(FestivalDetailModel.event_id == event_id).first()
        if db_festival_detail is None:
            db_festival_detail = FestivalDetailModel(event_id=event_id)
            db.add(db_festival_detail)
        db_festival_detail.accommodation = event.festival_detail.accommodation
        db_festival_detail.transport = event.festival_detail.transport
        db_festival_detail.merchandise = event.festival_detail.merchandise
        db_festival_detail.artist_payment = event.festival_detail.artist_payment

    if event.event_type == "Personal Concert" and event.concert_detail:
        db_concert_detail = db.query(ConcertDetailModel).filter(ConcertDetailModel.event_id == event_id).first()
        if db_concert_detail is None:
            db_concert_detail = ConcertDetailModel(event_id=event_id)
            db.add(db_concert_detail)
        db_concert_detail.accommodation = event.concert_detail.accommodation
        db_concert_detail.transport = event.concert_detail.transport
        db_concert_detail.ticket_price = event.concert_detail.ticket_price
        db_concert_detail.physical_tickets = event.concert_detail.physical_tickets
        db_concert_detail.electronic_tickets = event.concert_detail.electronic_tickets
        db_concert_detail.electronic_ticket_fee = event.concert_detail.electronic_ticket_fee
        db_concert_detail.culture_tax = event.concert_detail.culture_tax

    db.commit()
    return db_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    204: {
        "description": "Event deleted successfully"
    },
    404: {
        "description": "Event not found"
    }
}, dependencies=[Depends(get_current_active_user)])
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    db.query(FestivalDetailModel).filter(FestivalDetailModel.event_id == event_id).delete()
    db.query(ConcertDetailModel).filter(ConcertDetailModel.event_id == event_id).delete()
    db.delete(db_event)
    db.commit()
    return
