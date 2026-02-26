from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.event_service import fetch_events, fetch_event_with_seats

router = APIRouter(prefix="/events", tags=["Events"])

# GET /events → paginated list (cached in Redis)
@router.get("")
async def list_events(
    page  : int = Query(default=1,  ge=1),
    limit : int = Query(default=10, ge=1, le=100),
    db    : Session = Depends(get_db)
):
    return await fetch_events(db, page, limit)


# GET /events/{event_id} → event details + all seats grouped by category
@router.get("/{event_id}")
async def get_event(event_id: str, db: Session = Depends(get_db)):
    return await fetch_event_with_seats(db, event_id)