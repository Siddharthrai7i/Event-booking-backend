from fastapi import APIRouter
from app.api.v1 import auth, events

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(events.router)
# coming soon:
# router.include_router(booking.router)
# router.include_router(payment.router)
# future: router.include_router(events.router)
# future: router.include_router(booking.router)
# future: router.include_router(payment.router)