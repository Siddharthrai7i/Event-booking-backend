import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal
from app.db.session import get_db

# Import all models so SQLAlchemy registers them
from app.models.user    import User
from app.models.event   import Event
from app.models.seat    import Seat
from app.models.booking import Booking
from app.models.payment import Payment

from seeders.seed_events import seed_events
from seeders.seed_seats  import seed_seats


def run_seeds():
    db = SessionLocal()
    try:
        print("\n🌱 Starting database seeding...\n")

        # Order matters — events first, then seats
        seed_events(db)
        seed_seats(db)

        print("\n✅ All seeds completed successfully!\n")
    except Exception as e:
        db.rollback()
        print(f"\n❌ Seeding failed: {e}\n")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()