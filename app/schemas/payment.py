from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class PayRequest(BaseModel):
    booking_id      : UUID
    idempotency_key : str   # unique string sent by client e.g. "booking_uuid_attempt_1"


# ── Razorpay ─────────────────────────────────────────────────────────────────
class CreateOrderRequest(BaseModel):
    booking_id: UUID


class CreateOrderOut(BaseModel):
    order_id    : str
    key_id      : str
    amount      : float
    amount_paise: int
    currency    : str
    booking_id  : str


class VerifyPaymentRequest(BaseModel):
    booking_id           : UUID
    razorpay_payment_id  : str
    razorpay_order_id    : str
    razorpay_signature   : str


class PaymentOut(BaseModel):
    id              : UUID
    booking_id      : UUID
    amount          : Decimal
    status          : str
    idempotency_key : str
    created_at      : datetime

    class Config:
        from_attributes = True