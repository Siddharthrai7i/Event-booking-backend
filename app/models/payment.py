from sqlalchemy import Column, String, Enum, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.db.base import Base

class PaymentStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED  = "FAILED"

class Payment(Base):
    __tablename__ = "payments"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id      = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False)
    amount          = Column(Numeric(10, 2), nullable=False)
    status          = Column(Enum(PaymentStatus), nullable=False)
    idempotency_key = Column(String(255), unique=True, nullable=False)
    created_at      = Column(TIMESTAMP, server_default="now()", nullable=False)

    # Relationship
    booking = relationship("Booking", back_populates="payment",
                          foreign_keys=[booking_id])