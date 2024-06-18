# app/services/event_service.py
from sqlalchemy.orm import Session
from app.models import Event as EventModel, FestivalDetail as FestivalDetailModel, ConcertDetail as ConcertDetailModel
from app.schemas import EventCreate
from app.database import get_db


def create_event(event: EventCreate, db: Session):
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


def get_events(skip: int = 0, limit: int = 100, db: Session = None):
    return db.query(EventModel).offset(skip).limit(limit).all()


def get_event(event_id: int, db: Session):
    return db.query(EventModel).filter(event_id == EventModel.event_id).first()


def update_event(event_id: int, event: EventCreate, db: Session):
    db_event = db.query(EventModel).filter(event_id == EventModel.event_id).first()
    if db_event:
        db_event.name = event.name
        db_event.date = event.date
        db_event.location = event.location
        db_event.event_type = event.event_type

        if event.event_type == "Festival" and event.festival_detail:
            db_festival_detail = db.query(FestivalDetailModel).filter(event_id == FestivalDetailModel.event_id).first()
            if db_festival_detail is None:
                db_festival_detail = FestivalDetailModel(event_id=event_id)
                db.add(db_festival_detail)
            db_festival_detail.accommodation = event.festival_detail.accommodation
            db_festival_detail.transport = event.festival_detail.transport
            db_festival_detail.merchandise = event.festival_detail.merchandise
            db_festival_detail.artist_payment = event.festival_detail.artist_payment

        if event.event_type == "Personal Concert" and event.concert_detail:
            db_concert_detail = db.query(ConcertDetailModel).filter(event_id == ConcertDetailModel.event_id).first()
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


def delete_event(event_id: int, db: Session):
    db_event = db.query(EventModel).filter(event_id == EventModel.event_id).first()
    if db_event:
        db.query(FestivalDetailModel).filter(event_id == FestivalDetailModel.event_id).delete()
        db.query(ConcertDetailModel).filter(event_id == ConcertDetailModel.event_id).delete()
        db.delete(db_event)
        db.commit()

