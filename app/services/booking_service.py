from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.repositories.booking_repo import (
    create_booking,
    get_booking_by_id,
    get_bookings_by_user,
    update_booking_status
)
from app.repositories.seat_repo import (
    get_seat_with_lock,
    get_seat_by_id,
    update_seat_status
)
from app.models.booking import Booking, BookingStatus
from app.models.seat import SeatStatus
from app.models.user import User
from app.utils.exceptions import (
    SeatNotFoundException,
    SeatNotAvailableException,
    BookingNotFoundException,
    BookingNotOwnedException,
    BookingNotCancellableException,
    BookingExpiredException
)


def reserve_seat(db: Session, seat_id: str, current_user: User) -> Booking:

    # Step 1: Fetch seat with row lock
    # FOR UPDATE locks this row so no other request
    # can read or modify it until we commit
    seat = get_seat_with_lock(db, seat_id)

    # Step 2: Check seat exists
    if not seat:
        raise SeatNotFoundException()

    # Step 3: Check seat is available
    if seat.status != SeatStatus.AVAILABLE:
        raise SeatNotAvailableException()

    # Step 4: Mark seat as RESERVED
    seat.status = SeatStatus.RESERVED
    db.flush()   # write to DB but don't commit yet

    # Step 5: Create booking
    booking = create_booking(
        db       = db,
        user_id  = current_user.id,
        seat     = seat,
    )

    # Step 6: Commit everything together
    db.commit()
    db.refresh(booking)

    return booking


def get_booking(db: Session, booking_id: str, current_user: User) -> Booking:

    # Step 1: Fetch booking
    booking = get_booking_by_id(db, booking_id)

    # Step 2: Check booking exists
    if not booking:
        raise BookingNotFoundException()

    # Step 3: Check booking belongs to current user
    if str(booking.user_id) != str(current_user.id):
        raise BookingNotOwnedException()

    return booking


def get_my_bookings(db: Session, current_user: User) -> list[Booking]:
    return get_bookings_by_user(db, current_user.id)


def cancel_booking(db: Session, booking_id: str, current_user: User):

    # Step 1: Fetch booking
    booking = get_booking_by_id(db, booking_id)

    # Step 2: Check booking exists
    if not booking:
        raise BookingNotFoundException()

    # Step 3: Check booking belongs to current user
    if str(booking.user_id) != str(current_user.id):
        raise BookingNotOwnedException()

    # Step 4: Check booking is PENDING
    if booking.status != BookingStatus.PENDING:
        raise BookingNotCancellableException()

    # Step 5: Release seat back to AVAILABLE
    seat = get_seat_by_id(db, str(booking.seat_id))
    update_seat_status(db, seat, SeatStatus.AVAILABLE)

    # Step 6: Cancel booking
    update_booking_status(db, booking, BookingStatus.CANCELLED)

    return {"message": "Booking cancelled successfully ✅"}