from sqlalchemy import Column, String, Enum, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.db.base import Base

class SeatCategory(str, enum.Enum):
    VIP     = "VIP"
    PREMIUM = "PREMIUM"
    GENERAL = "GENERAL"

class SeatStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED  = "RESERVED"
    BOOKED    = "BOOKED"

class Seat(Base):
    __tablename__ = "seats"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id    = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    seat_number = Column(String(20), nullable=False)
    category    = Column(Enum(SeatCategory), nullable=False)
    price       = Column(Numeric(10, 2), nullable=False)
    status      = Column(Enum(SeatStatus), nullable=False,
                        default=SeatStatus.AVAILABLE,
                        server_default="AVAILABLE")

    # Relationships
    event   = relationship("Event", back_populates="seats")
    booking = relationship("Booking", back_populates="seat", uselist=False)