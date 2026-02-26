import json
from sqlalchemy.orm import Session
from app.repositories.event_repo import get_all_events, get_event_by_id
from app.repositories.seat_repo import get_seats_by_event
from app.db.redis import redis_client
from fastapi import HTTPException, status

EVENTS_CACHE_KEY = "events:page:{page}:limit:{limit}"
EVENTS_CACHE_TTL = 300  # 5 minutes


async def fetch_events(db: Session, page: int = 1, limit: int = 10):
    cache_key = EVENTS_CACHE_KEY.format(page=page, limit=limit)

    # Step 1: Check Redis cache
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)     # Cache HIT ⚡

    # Step 2: Cache MISS → query DB
    events, total = get_all_events(db, page, limit)

    result = {
        "events": [
            {
                "id"   : str(e.id),
                "name" : e.name,
                "city" : e.city,
                "venue": e.venue,
                "date" : str(e.date),
            }
            for e in events
        ],
        "total": total,
        "page" : page,
        "limit": limit,
    }

    # Step 3: Store in Redis for 5 minutes
    await redis_client.setex(cache_key, EVENTS_CACHE_TTL, json.dumps(result))

    return result


async def fetch_event_with_seats(db: Session, event_id: str):
    # Step 1: Get event
    event = get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # Step 2: Get all seats for this event
    seats = get_seats_by_event(db, event_id)

    # Step 3: Group seats by category
    grouped = {}
    for seat in seats:
        cat = seat.category.value
        if cat not in grouped:
            grouped[cat] = {
                "price": float(seat.price),
                "seats": []
            }
        grouped[cat]["seats"].append({
            "id"          : str(seat.id),
            "seat_number" : seat.seat_number,
            "status"      : seat.status.value,
            "price"       : float(seat.price),
            "category"    : seat.category.value,
        })

    return {
        "event": {
            "id"   : str(event.id),
            "name" : event.name,
            "city" : event.city,
            "venue": event.venue,
            "date" : str(event.date),
        },
        "seats": grouped
    }