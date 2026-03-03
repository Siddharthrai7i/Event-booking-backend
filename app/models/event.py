from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name       = Column(String(255), nullable=False)
    city       = Column(String(100), nullable=False)
    venue      = Column(String(255), nullable=False)
    date       = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()", nullable=False)

    # Relationship
    seats = relationship("Seat", back_populates="event")