from sqlalchemy.orm import Session
from app.models.booking import Booking, BookingStatus
from app.models.seat import Seat, SeatStatus
from datetime import datetime, timedelta, timezone
import uuid

def create_booking(db: Session, user_id: str, seat: Seat) -> Booking:
    booking = Booking(
        id         = uuid.uuid4(),
        user_id    = user_id,
        seat_id    = seat.id,
        amount     = seat.price,          # copy price from seat
        status     = BookingStatus.PENDING,
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_booking_by_id(db: Session, booking_id: str) -> Booking | None:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings_by_user(db: Session, user_id: str) -> list[Booking]:
    return db.query(Booking)\
             .filter(Booking.user_id == user_id)\
             .order_by(Booking.created_at.desc())\
             .all()

def update_booking_status(db: Session, booking: Booking, 
                          status: BookingStatus) -> Booking:
    booking.status = status
    db.commit()
    db.refresh(booking)
    return booking