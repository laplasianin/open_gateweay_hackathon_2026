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


@router.post("/reset/{event_id}")
async def reset_simulation(event_id: UUID):
    from app.services.simulation import stop_simulation as _stop, _reset_entities
    from app.database import async_session
    from sqlalchemy import delete
    from app.models.incident import Incident

    await _stop(str(event_id))
    await _reset_entities(str(event_id))
    # Clear all incidents for this event
    async with async_session() as db:
        await db.execute(delete(Incident).where(Incident.event_id == event_id))
        await db.commit()
    return {"status": "reset", "event_id": str(event_id)}


@router.get("/status/{event_id}")
async def simulation_status(event_id: UUID):
    from app.services.simulation import _running
    running = _running.get(str(event_id), False)
    return {"running": running, "event_id": str(event_id)}
