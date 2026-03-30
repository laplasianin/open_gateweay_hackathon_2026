import math
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident
from app.models.staff import Staff
from app.schemas.incident import SosRequest
from app.services.qod import activate_qod
from app.services.ws_manager import ws_manager


def _distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_nearest_medic(staff: list[dict], lat: float, lng: float) -> dict | None:
    medics = [s for s in staff if s["role"] == "medical" and s.get("current_lat") is not None]
    if not medics:
        return None
    return min(medics, key=lambda s: _distance(lat, lng, s["current_lat"], s["current_lng"]))


async def handle_sos(db: AsyncSession, request: SosRequest) -> Incident:
    from app.models.visitor import Visitor

    # Get visitor to find event_id
    visitor_result = await db.execute(select(Visitor).where(Visitor.id == request.visitor_id))
    visitor = visitor_result.scalar_one()

    # Find nearest medic
    result = await db.execute(select(Staff).where(Staff.event_id == visitor.event_id, Staff.role == "medical"))
    medics_models = result.scalars().all()
    staff_dicts = [
        {"id": str(m.id), "role": m.role, "current_lat": m.current_lat, "current_lng": m.current_lng}
        for m in medics_models
    ]
    medic_dict = find_nearest_medic(staff_dicts, request.lat, request.lng)

    incident = Incident(
        event_id=visitor.event_id,
        type="medical_emergency",
        status="responding" if medic_dict else "open",
        reporter_id=request.visitor_id,
        responder_id=UUID(medic_dict["id"]) if medic_dict else None,
        lat=request.lat,
        lng=request.lng,
    )
    db.add(incident)

    # Activate QoD for medic
    if medic_dict:
        medic_model = await db.get(Staff, UUID(medic_dict["id"]))
        if medic_model and medic_model.qod_status != "active":
            session_id = await activate_qod(medic_model.device_id, "medical")
            medic_model.qod_status = "active"
            medic_model.qod_session_id = session_id

    await db.commit()
    await db.refresh(incident)

    # Broadcast
    dist = _distance(request.lat, request.lng, medic_dict["current_lat"], medic_dict["current_lng"]) if medic_dict else None
    await ws_manager.broadcast(
        str(visitor.event_id),
        {
            "type": "incident",
            "data": {
                "id": str(incident.id),
                "lat": incident.lat,
                "lng": incident.lng,
                "status": incident.status,
                "responder_id": str(incident.responder_id) if incident.responder_id else None,
                "distance_meters": round(dist) if dist else None,
            },
        },
    )
    await ws_manager.broadcast(
        str(visitor.event_id),
        {
            "type": "log",
            "data": {
                "message": f"SOS received! Nearest medic dispatched ({round(dist)}m away)" if dist else "SOS received! No medic available",
                "level": "critical",
            },
        },
    )

    return incident


async def resolve_incident(db: AsyncSession, incident_id: UUID) -> Incident:
    incident = await db.get(Incident, incident_id)
    incident.status = "resolved"
    incident.resolved_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(incident)

    await ws_manager.broadcast(
        str(incident.event_id),
        {"type": "incident", "data": {"id": str(incident.id), "status": "resolved"}},
    )
    await ws_manager.broadcast(
        str(incident.event_id),
        {"type": "log", "data": {"message": "Incident resolved", "level": "success"}},
    )
    return incident
