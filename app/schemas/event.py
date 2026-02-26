from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class EventOut(BaseModel):
    id    : UUID
    name  : str
    city  : str
    venue : str
    date  : datetime

    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    events : list[EventOut]
    total  : int
    page   : int
    limit  : int