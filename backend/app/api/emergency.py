import traceback
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.incident import IncidentResponse, SosRequest
from app.services.emergency import handle_sos, resolve_incident

router = APIRouter(prefix="/api/emergency", tags=["emergency"])


@router.post("/sos", response_model=IncidentResponse)
async def trigger_sos(request: SosRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await handle_sos(db, request)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/active/{staff_id}", response_model=IncidentResponse | None)
async def get_active_incident(staff_id: UUID, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    from app.models.incident import Incident
    result = await db.execute(
        select(Incident).where(Incident.responder_id == staff_id, Incident.status != "resolved").limit(1)
    )
    return result.scalar_one_or_none()


@router.post("/{incident_id}/resolve", response_model=IncidentResponse)
async def resolve(incident_id: UUID, db: AsyncSession = Depends(get_db)):
    return await resolve_incident(db, incident_id)
