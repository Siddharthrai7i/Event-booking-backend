from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime

class PayRequest(BaseModel):
    booking_id      : UUID
    idempotency_key : str   # unique string sent by client e.g. "booking_uuid_attempt_1"

class PaymentOut(BaseModel):
    id              : UUID
    booking_id      : UUID
    amount          : Decimal
    status          : str
    idempotency_key : str
    created_at      : datetime

    class Config:
        from_attributes = True