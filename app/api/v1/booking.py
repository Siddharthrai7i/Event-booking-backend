from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.booking import ReserveRequest, CancelRequest, BookingOut
from app.services.booking_service import (
    reserve_seat,
    get_booking,
    get_my_bookings,
    cancel_booking
)
from app.core.dependencies import get_verified_user
from app.models.user import User

router = APIRouter(prefix="/booking", tags=["Booking"])


# POST /booking/reserve → reserve a seat
@router.post("/reserve", response_model=BookingOut, status_code=201)
def reserve(
    payload      : ReserveRequest,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    return reserve_seat(db, str(payload.seat_id), current_user)


# GET /booking/my-bookings → get all bookings of current user
@router.get("/my-bookings")
def my_bookings(
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    return get_my_bookings(db, current_user)


# GET /booking/{booking_id} → get single booking details
@router.get("/{booking_id}", response_model=BookingOut)
def get_booking_details(
    booking_id   : str,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    return get_booking(db, booking_id, current_user)



@router.post("/cancel")
def cancel(
    payload      : CancelRequest,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    return cancel_booking(db, str(payload.booking_id), current_user)