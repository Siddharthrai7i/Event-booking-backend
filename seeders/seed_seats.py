from app.models.seat import Seat, SeatCategory, SeatStatus
from app.models.event import Event
import uuid

def seed_seats(db):
    # Check if seats already exist
    existing = db.query(Seat).count()
    if existing > 0:
        print("Seats already seeded — skipping")
        return

    events = db.query(Event).all()
    if not events:
        print("No events found — seed events first")
        return

    all_seats = []

    # Seat config per category
    seat_config = [
        # (category,          price,   prefix, count)
        (SeatCategory.VIP,     5000.00, "A",    10),
        (SeatCategory.PREMIUM, 2500.00, "B",    20),
        (SeatCategory.GENERAL, 800.00,  "C",    50),
    ]

    for event in events:
        for category, price, prefix, count in seat_config:
            for i in range(1, count + 1):
                seat = Seat(
                    id          = uuid.uuid4(),
                    event_id    = event.id,
                    seat_number = f"{prefix}{i}",
                    category    = category,
                    price       = price,
                    status      = SeatStatus.AVAILABLE,
                )
                all_seats.append(seat)

    db.add_all(all_seats)
    db.commit()
    print(f"✅ Seeded {len(all_seats)} seats across {len(events)} events")
    print(f"   Per event: 10 VIP + 20 Premium + 50 General = 80 seats")