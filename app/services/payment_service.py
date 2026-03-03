import random
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.repositories.booking_repo import (
    get_booking_by_id,
    update_booking_status
)
from app.repositories.payment_repo import (
    get_payment_by_idempotency_key,
    get_payment_by_booking_id,
    create_payment
)
from app.repositories.seat_repo import (
    get_seat_by_id,
    update_seat_status
)
from app.repositories.event_repo import get_event_by_id
from app.repositories.user_repo import get_user_by_id
from app.models.booking import BookingStatus
from app.models.payment import PaymentStatus
from app.models.seat import SeatStatus
from app.models.user import User
from app.utils.exceptions import (
    BookingNotFoundException,
    BookingNotOwnedException,
    BookingExpiredException,
    DuplicatePaymentException,
    BookingAlreadyPaidException,
    PaymentNotFoundException
)
from app.utils.email import send_booking_confirmation_email


def simulate_payment() -> bool:
    return random.random() < 0.9


async def process_payment(
    db              : Session,
    booking_id      : str,
    idempotency_key : str,
    current_user    : User
):
    # ── Step 1: Fetch booking ─────────────────────
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise BookingNotFoundException()

    # ── Step 2: Check booking belongs to user ─────
    if str(booking.user_id) != str(current_user.id):
        raise BookingNotOwnedException()

    # ── Step 3: Check booking status ──────────────
    if booking.status == BookingStatus.CONFIRMED:
        raise BookingAlreadyPaidException()

    if booking.status == BookingStatus.CANCELLED:
        raise BookingNotFoundException()

    # ── Step 4: Check booking not expired ─────────
    now        = datetime.now(timezone.utc)
    expires_at = booking.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if now > expires_at:
        update_booking_status(db, booking, BookingStatus.CANCELLED)
        seat = get_seat_by_id(db, str(booking.seat_id))
        update_seat_status(db, seat, SeatStatus.AVAILABLE)
        raise BookingExpiredException()

    # ── Step 5: Check idempotency key ─────────────
    existing_payment = get_payment_by_idempotency_key(db, idempotency_key)
    if existing_payment:
        raise DuplicatePaymentException()

    # ── Step 6: Check not already paid ────────────
    existing = get_payment_by_booking_id(db, booking_id)
    if existing and existing.status == PaymentStatus.SUCCESS:
        raise BookingAlreadyPaidException()

    # ── Step 7: Simulate payment ──────────────────
    payment_success = simulate_payment()

    if payment_success:
        # ── Step 8a: SUCCESS ──────────────────────
        update_booking_status(db, booking, BookingStatus.CONFIRMED)

        seat = get_seat_by_id(db, str(booking.seat_id))
        update_seat_status(db, seat, SeatStatus.BOOKED)

        payment = create_payment(
            db              = db,
            booking_id      = booking_id,
            amount          = float(booking.amount),
            status          = PaymentStatus.SUCCESS,
            idempotency_key = idempotency_key
        )

        # ── Step 9: Send confirmation email ───────
        event = get_event_by_id(db, str(seat.event_id))
        user  = get_user_by_id(db, str(current_user.id))

        await send_booking_confirmation_email(
            email       = user.email,
            user_name   = user.email.split("@")[0],   # use part before @
            event_name  = event.name,
            event_city  = event.city,
            event_venue = event.venue,
            event_date  = event.date.strftime("%d %B %Y, %I:%M %p"),
            seat_number = seat.seat_number,
            category    = seat.category.value,
            amount      = float(booking.amount),
            booking_id  = str(booking.id),
            payment_id  = str(payment.id),
            paid_on     = datetime.now(timezone.utc).strftime("%d %B %Y, %I:%M %p")
        )

        return {
            "status"         : "SUCCESS ✅",
            "message"        : "Payment successful! Booking confirmed. Check your email.",
            "booking_id"     : str(booking.id),
            "payment_id"     : str(payment.id),
            "amount_paid"    : float(booking.amount),
            "booking_status" : "CONFIRMED",
            "seat_status"    : "BOOKED",
        }

    else:
        # ── Step 8b: FAILED ───────────────────────
        update_booking_status(db, booking, BookingStatus.CANCELLED)

        seat = get_seat_by_id(db, str(booking.seat_id))
        update_seat_status(db, seat, SeatStatus.AVAILABLE)

        payment = create_payment(
            db              = db,
            booking_id      = booking_id,
            amount          = float(booking.amount),
            status          = PaymentStatus.FAILED,
            idempotency_key = idempotency_key
        )

        return {
            "status"         : "FAILED ❌",
            "message"        : "Payment failed. Please try again with a new reservation.",
            "booking_id"     : str(booking.id),
            "payment_id"     : str(payment.id),
            "amount"         : float(booking.amount),
            "booking_status" : "CANCELLED",
            "seat_status"    : "AVAILABLE",
        }


def get_payment_details(
    db          : Session,
    booking_id  : str,
    current_user: User
):
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise BookingNotFoundException()

    if str(booking.user_id) != str(current_user.id):
        raise BookingNotOwnedException()

    payment = get_payment_by_booking_id(db, booking_id)
    if not payment:
        raise PaymentNotFoundException()

    return payment