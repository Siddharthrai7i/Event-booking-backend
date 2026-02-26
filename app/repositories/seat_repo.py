from sqlalchemy.orm import Session
from app.models.seat import Seat, SeatStatus

def get_seats_by_event(db: Session, event_id: str) -> list[Seat]:
    return db.query(Seat).filter(Seat.event_id == event_id).all()

def get_seat_by_id(db: Session, seat_id: str) -> Seat | None:
    return db.query(Seat).filter(Seat.id == seat_id).first()

def get_seat_with_lock(db: Session, seat_id: str) -> Seat | None:
    # FOR UPDATE locks the row — prevents double booking
    return db.query(Seat)\
             .filter(Seat.id == seat_id)\
             .with_for_update()\
             .first()

def update_seat_status(db: Session, seat: Seat, status: SeatStatus) -> Seat:
    seat.status = status
    db.commit()
    db.refresh(seat)
    return seat