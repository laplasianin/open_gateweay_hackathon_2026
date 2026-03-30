from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.incident import IncidentResponse, SosRequest
from app.services.emergency import handle_sos, resolve_incident

router = APIRouter(prefix="/api/emergency", tags=["emergency"])


@router.post("/sos", response_model=IncidentResponse)
async def trigger_sos(request: SosRequest, db: AsyncSession = Depends(get_db)):
    return await handle_sos(db, request)


@router.post("/{incident_id}/resolve", response_model=IncidentResponse)
async def resolve(incident_id: UUID, db: AsyncSession = Depends(get_db)):
    return await resolve_incident(db, incident_id)
