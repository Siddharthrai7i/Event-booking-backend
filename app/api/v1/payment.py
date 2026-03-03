from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.payment import PayRequest, PaymentOut
from app.services.payment_service import process_payment, get_payment_details
from app.core.dependencies import get_verified_user
from app.models.user import User

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/pay")
async def pay(
    payload      : PayRequest,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    result = await process_payment(
        db              = db,
        booking_id      = str(payload.booking_id),
        idempotency_key = payload.idempotency_key,
        current_user    = current_user
    )
    return result   # ← return the result not the coroutine


@router.get("/{booking_id}", response_model=PaymentOut)
def get_payment(
    booking_id   : str,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_verified_user)
):
    return get_payment_details(db, booking_id, current_user)