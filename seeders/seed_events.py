from app.models.event import Event
from datetime import datetime
import uuid

def seed_events(db):
    # Check if events already exist
    existing = db.query(Event).count()
    if existing > 0:
        print("Events already seeded — skipping")
        return

    events = [
        Event(
            id    = uuid.uuid4(),
            name  = "Coldplay Music of the Spheres",
            city  = "Mumbai",
            venue = "DY Patil Stadium",
            date  = datetime(2025, 3, 15, 19, 0, 0),
        ),
        Event(
            id    = uuid.uuid4(),
            name  = "Arijit Singh Live Concert",
            city  = "Delhi",
            venue = "Jawaharlal Nehru Stadium",
            date  = datetime(2025, 4, 20, 18, 0, 0),
        ),
        Event(
            id    = uuid.uuid4(),
            name  = "AR Rahman Live",
            city  = "Bangalore",
            venue = "Palace Grounds",
            date  = datetime(2025, 5, 10, 17, 0, 0),
        ),
        Event(
            id    = uuid.uuid4(),
            name  = "IPL Final 2025",
            city  = "Chennai",
            venue = "MA Chidambaram Stadium",
            date  = datetime(2025, 6, 1, 20, 0, 0),
        ),
        Event(
            id    = uuid.uuid4(),
            name  = "Sunburn Festival",
            city  = "Goa",
            venue = "Vagator Beach",
            date  = datetime(2025, 12, 27, 16, 0, 0),
        ),
    ]

    db.add_all(events)
    db.commit()
    print(f"✅ Seeded {len(events)} events")
    return events