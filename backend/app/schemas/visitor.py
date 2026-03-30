from uuid import UUID
from pydantic import BaseModel


class VisitorResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    type: str
    device_id: str
    qod_status: str
    qod_session_id: str | None
    current_lat: float | None
    current_lng: float | None
    current_zone_id: UUID | None
    model_config = {"from_attributes": True}
