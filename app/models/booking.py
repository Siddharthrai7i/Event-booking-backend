from sqlalchemy import Column, Enum, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.db.base import Base

class BookingStatus(str, enum.Enum):
    PENDING   = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Booking(Base):
    __tablename__ = "bookings"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    seat_id    = Column(UUID(as_uuid=True), ForeignKey("seats.id"), nullable=False)
    amount     = Column(Numeric(10, 2), nullable=False)
    status     = Column(Enum(BookingStatus), nullable=False,
                       default=BookingStatus.PENDING,
                       server_default="PENDING")
    payment_id = Column(UUID(as_uuid=True), nullable=True)  # ← No FK yet, added later
    expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()", nullable=False)

    # Relationships
    user    = relationship("User", back_populates="bookings")
    seat    = relationship("Seat", back_populates="booking")
    payment = relationship("Payment", back_populates="booking",
                          primaryjoin="Booking.payment_id == Payment.id",
                          foreign_keys="Booking.payment_id")