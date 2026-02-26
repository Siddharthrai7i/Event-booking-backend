from sqlalchemy import Column, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.db.base import Base

class UserRole(str, enum.Enum):
    user  = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email         = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role          = Column(Enum(UserRole), nullable=False, default=UserRole.user, server_default="user")
    is_verified   = Column(Boolean, nullable=False, default=False, server_default="false")

    bookings = relationship("Booking", back_populates="user")