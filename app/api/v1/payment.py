from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.payment import PayRequest, PaymentOut, CreateOrderOut, CreateOrderRequest, VerifyPaymentRequest
from app.services.payment_service import (
    process_payment,
    get_payment_details,
    create_razorpay_order,
    verify_razorpay_payment,
)
from app.core.dependencies import get_verified_user
from app.models.user import User

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/pay")
async def pay(
    payload      : PayRequest,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    """Legacy simulated payment (optional). Prefer Razorpay: create-order → client checkout → verify."""
    result = await process_payment(
        db              = db,
        booking_id      = str(payload.booking_id),
        idempotency_key = payload.idempotency_key,
        current_user    = current_user
    )
    return result


# ── Razorpay ─────────────────────────────────────────────────────────────────

@router.post("/create-order", response_model=CreateOrderOut)
def razorpay_create_order(
    payload      : CreateOrderRequest,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    """Create a Razorpay order for the given booking. Use returned order_id and key_id in Flutter/client checkout."""
    return create_razorpay_order(db, str(payload.booking_id), current_user)


@router.post("/verify")
async def razorpay_verify(
    payload      : VerifyPaymentRequest,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    """Verify Razorpay payment after successful checkout. Call this with payment_id, order_id, signature from client."""
    return await verify_razorpay_payment(
        db                  = db,
        booking_id          = str(payload.booking_id),
        razorpay_payment_id = payload.razorpay_payment_id,
        razorpay_order_id   = payload.razorpay_order_id,
        razorpay_signature  = payload.razorpay_signature,
        current_user        = current_user
    )


@router.get("/{booking_id}", response_model=PaymentOut)
def get_payment(
    booking_id   : str,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    return get_payment_details(db, booking_id, current_user)