from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class SosRequest(BaseModel):
    visitor_id: UUID
    lat: float
    lng: float


class IncidentResponse(BaseModel):
    id: UUID
    event_id: UUID
    type: str
    status: str
    reporter_id: UUID | None
    responder_id: UUID | None
    lat: float
    lng: float
    created_at: datetime
    resolved_at: datetime | None
    model_config = {"from_attributes": True}
