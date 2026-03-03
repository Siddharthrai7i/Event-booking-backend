from app.db.base import SessionLocal

# Import all models here so SQLAlchemy registers all relationships
from app.models.user    import User     # noqa
from app.models.event   import Event    # noqa
from app.models.seat    import Seat     # noqa
from app.models.booking import Booking  # noqa
from app.models.payment import Payment  # noqa

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()