from uuid import UUID
from pydantic import BaseModel


class ZoneResponse(BaseModel):
    id: UUID
    name: str
    type: str
    polygon: list[list[float]]
    crowd_level: str
    color: str
    model_config = {"from_attributes": True}


class EventResponse(BaseModel):
    id: UUID
    name: str
    description: str
    city: str
    country: str
    bounds: dict
    status: str
    zones: list[ZoneResponse] = []
    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    id: UUID
    name: str
    city: str
    country: str
    status: str
    model_config = {"from_attributes": True}
