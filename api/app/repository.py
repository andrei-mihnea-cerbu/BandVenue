from sqlalchemy.orm import Session
from app.models import Artist, Event, User


class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, db: Session, elem_id: int):
        return db.query(self.model).filter(self.model.id == elem_id).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, obj):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj):
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj):
        db.delete(obj)
        db.commit()


class ArtistRepository(BaseRepository):
    def __init__(self):
        super().__init__(Artist)


class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__(Event)


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
