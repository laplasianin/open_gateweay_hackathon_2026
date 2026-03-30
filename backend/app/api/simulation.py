from uuid import UUID
from fastapi import APIRouter

router = APIRouter(prefix="/api/simulation", tags=["simulation"])


@router.post("/start/{event_id}")
async def start_simulation(event_id: UUID):
    from app.services.simulation import start_simulation as _start
    await _start(str(event_id))
    return {"status": "started", "event_id": str(event_id)}


@router.post("/stop/{event_id}")
async def stop_simulation(event_id: UUID):
    from app.services.simulation import stop_simulation as _stop
    await _stop(str(event_id))
    return {"status": "stopped", "event_id": str(event_id)}
