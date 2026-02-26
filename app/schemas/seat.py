from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class SeatOut(BaseModel):
    id          : UUID
    seat_number : str
    category    : str
    price       : Decimal
    status      : str

    class Config:
        from_attributes = True

class SeatsByCategoryOut(BaseModel):
    price : Decimal
    seats : list[SeatOut]

class EventSeatsResponse(BaseModel):
    event : dict
    seats : dict[str, SeatsByCategoryOut]