from sqlalchemy.orm import Session
from app.models.event import Event

def get_all_events(db: Session, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    events = db.query(Event).offset(offset).limit(limit).all()
    total  = db.query(Event).count()
    return events, total

def get_event_by_id(db: Session, event_id: str) -> Event | None:
    return db.query(Event).filter(Event.id == event_id).first()