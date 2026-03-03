from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime

# ── Request schemas ──────────────────────────────
class ReserveRequest(BaseModel):
    seat_id: UUID

class CancelRequest(BaseModel):
    booking_id: UUID

# ── Response schemas ─────────────────────────────
class BookingOut(BaseModel):
    id         : UUID
    seat_id    : UUID
    amount     : Decimal
    status     : str
    expires_at : datetime
    created_at : datetime

    class Config:
        from_attributes = True