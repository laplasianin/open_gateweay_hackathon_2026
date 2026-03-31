import asyncio
import math
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.event import Zone
from app.models.incident import Incident
from app.models.simulation_path import SimulationPath
from app.models.staff import Staff
from app.models.visitor import Visitor
from app.services.geofence import find_zone
from app.services.qod import activate_qod, deactivate_qod
from app.services.ws_manager import ws_manager

# Medic override targets: {staff_id_str: {"lat": float, "lng": float, "incident_id": str}}
_medic_overrides: dict[str, dict] = {}

MEDIC_SPEED = 0.0001  # ~11m per tick in lat/lng degrees
RESOLVE_DISTANCE_M = 20

_tasks: dict[str, asyncio.Task] = {}
_running: dict[str, bool] = {}

CROWD_SCRIPT = {
    30: {"Main Stage A": "high"},
    45: {"Main Stage A": "critical"},
    60: {"Medium Stage 1": "high"},
}


def _haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def dispatch_medic_to_incident(staff_id: str, lat: float, lng: float, incident_id: str):
    """Called from emergency service to redirect a medic toward an SOS location."""
    _medic_overrides[staff_id] = {"lat": lat, "lng": lng, "incident_id": incident_id}


def interpolate_position(waypoints: list[dict], elapsed: float) -> tuple[float, float]:
    if not waypoints:
        return (0.0, 0.0)

    # Loop: total duration is last waypoint offset
    total_duration = waypoints[-1]["offset"]
    if total_duration > 0 and elapsed > total_duration:
        elapsed = elapsed % total_duration

    if elapsed <= waypoints[0]["offset"]:
        return (waypoints[0]["lat"], waypoints[0]["lng"])
    for i in range(len(waypoints) - 1):
        wp1 = waypoints[i]
        wp2 = waypoints[i + 1]
        if wp1["offset"] <= elapsed <= wp2["offset"]:
            t = (elapsed - wp1["offset"]) / (wp2["offset"] - wp1["offset"])
            lat = wp1["lat"] + t * (wp2["lat"] - wp1["lat"])
            lng = wp1["lng"] + t * (wp2["lng"] - wp1["lng"])
            return (lat, lng)
    last = waypoints[-1]
    return (last["lat"], last["lng"])


async def _tick(event_id: str, elapsed: float, db: AsyncSession):
    zone_result = await db.execute(select(Zone).where(Zone.event_id == event_id))
    zones = zone_result.scalars().all()
    zone_dicts = [{"id": str(z.id), "name": z.name, "polygon": z.polygon} for z in zones]
    zone_map = {str(z.id): z for z in zones}
    zone_name_map = {z.name: z for z in zones}

    path_result = await db.execute(select(SimulationPath).where(SimulationPath.event_id == event_id))
    paths = path_result.scalars().all()

    for path in paths:
        # Skip scripted path if medic is dispatched to SOS
        if path.entity_type == "staff" and str(path.entity_id) in _medic_overrides:
            continue

        lat, lng = interpolate_position(path.waypoints, elapsed)

        if path.entity_type == "staff":
            entity = await db.get(Staff, path.entity_id)
        else:
            entity = await db.get(Visitor, path.entity_id)

        if entity is None:
            continue

        old_zone_id = str(entity.current_zone_id) if entity.current_zone_id else None
        new_zone_id = find_zone(lat, lng, zone_dicts)

        entity.current_lat = lat
        entity.current_lng = lng
        entity.current_zone_id = new_zone_id

        # Zone enter
        if new_zone_id and new_zone_id != old_zone_id:
            zone_name = zone_map[new_zone_id].name if new_zone_id in zone_map else "Unknown"
            role = entity.role if hasattr(entity, "role") else entity.type
            device_id = entity.device_id or f"device-{entity.id}"

            session_id = await activate_qod(device_id, role)
            entity.qod_status = "active"
            entity.qod_session_id = session_id

            await ws_manager.broadcast(event_id, {
                "type": "qod_update",
                "data": {"entity_id": str(entity.id), "entity_type": path.entity_type, "qod_status": "active", "session_id": session_id},
            })
            await ws_manager.broadcast(event_id, {
                "type": "log",
                "data": {"message": f"QoD activated for {entity.name} (entered {zone_name})", "level": "success"},
            })

        # Zone exit
        if old_zone_id and not new_zone_id and entity.qod_status == "active":
            if entity.qod_session_id:
                await deactivate_qod(entity.qod_session_id)
            entity.qod_status = "inactive"
            entity.qod_session_id = None

            await ws_manager.broadcast(event_id, {
                "type": "qod_update",
                "data": {"entity_id": str(entity.id), "entity_type": path.entity_type, "qod_status": "inactive"},
            })
            await ws_manager.broadcast(event_id, {
                "type": "log",
                "data": {"message": f"QoD deactivated for {entity.name} (exited zone)", "level": "info"},
            })

        # Position update
        await ws_manager.broadcast(event_id, {
            "type": "position_update",
            "data": {
                "entity_id": str(entity.id),
                "entity_type": path.entity_type,
                "lat": lat,
                "lng": lng,
                "zone_id": new_zone_id,
            },
        })

    # Move medics toward SOS and auto-resolve
    for staff_id, target in list(_medic_overrides.items()):
        medic = await db.get(Staff, staff_id)
        if medic is None or medic.current_lat is None:
            continue

        dist = _haversine(medic.current_lat, medic.current_lng, target["lat"], target["lng"])

        if dist <= RESOLVE_DISTANCE_M:
            # Auto-resolve incident
            incident = await db.get(Incident, target["incident_id"])
            if incident and incident.status != "resolved":
                incident.status = "resolved"
                incident.resolved_at = datetime.now(timezone.utc)
                await ws_manager.broadcast(event_id, {
                    "type": "incident",
                    "data": {"id": str(incident.id), "status": "resolved"},
                })
                await ws_manager.broadcast(event_id, {
                    "type": "log",
                    "data": {"message": f"Medic {medic.name} reached patient — incident resolved", "level": "success"},
                })
            del _medic_overrides[staff_id]
        else:
            # Move medic toward target
            dlat = target["lat"] - medic.current_lat
            dlng = target["lng"] - medic.current_lng
            length = math.sqrt(dlat ** 2 + dlng ** 2)
            if length > 0:
                medic.current_lat += (dlat / length) * MEDIC_SPEED
                medic.current_lng += (dlng / length) * MEDIC_SPEED

                await ws_manager.broadcast(event_id, {
                    "type": "position_update",
                    "data": {
                        "entity_id": str(medic.id),
                        "entity_type": "staff",
                        "lat": medic.current_lat,
                        "lng": medic.current_lng,
                        "zone_id": str(medic.current_zone_id) if medic.current_zone_id else None,
                    },
                })

    # Fake crowd levels
    elapsed_int = int(elapsed)
    if elapsed_int in CROWD_SCRIPT:
        for zone_name, level in CROWD_SCRIPT[elapsed_int].items():
            if zone_name in zone_name_map:
                zone = zone_name_map[zone_name]
                zone.crowd_level = level
                await ws_manager.broadcast(event_id, {
                    "type": "zone_update",
                    "data": {"zone_id": str(zone.id), "crowd_level": level},
                })
                if level in ("high", "critical"):
                    await ws_manager.broadcast(event_id, {
                        "type": "log",
                        "data": {
                            "message": f"AI Alert: {zone_name} crowd density {level.upper()} — recommend staff reinforcement",
                            "level": "warning" if level == "high" else "critical",
                        },
                    })

    await db.commit()


async def _run_simulation(event_id: str):
    start_time = asyncio.get_event_loop().time()
    _running[event_id] = True

    while _running.get(event_id, False):
        elapsed = asyncio.get_event_loop().time() - start_time
        async with async_session() as db:
            await _tick(event_id, elapsed, db)
        await asyncio.sleep(2)


async def _reset_entities(event_id: str):
    """Reset all positions, QoD statuses, and incidents for a fresh simulation run."""
    async with async_session() as db:
        # Reset staff
        result = await db.execute(select(Staff).where(Staff.event_id == event_id))
        for s in result.scalars().all():
            s.current_lat = None
            s.current_lng = None
            s.current_zone_id = None
            s.qod_status = "inactive"
            s.qod_session_id = None
        # Reset visitors
        result = await db.execute(select(Visitor).where(Visitor.event_id == event_id))
        for v in result.scalars().all():
            v.current_lat = None
            v.current_lng = None
            v.current_zone_id = None
            v.qod_status = "inactive"
            v.qod_session_id = None
        # Reset zones crowd level
        result = await db.execute(select(Zone).where(Zone.event_id == event_id))
        for z in result.scalars().all():
            z.crowd_level = "low"
        await db.commit()
    # Clear medic overrides
    _medic_overrides.clear()


async def start_simulation(event_id: str):
    if event_id in _tasks and not _tasks[event_id].done():
        # Stop existing first
        await stop_simulation(event_id)
    await _reset_entities(event_id)
    _tasks[event_id] = asyncio.create_task(_run_simulation(event_id))


async def stop_simulation(event_id: str):
    _running[event_id] = False
    if event_id in _tasks:
        _tasks[event_id].cancel()
        del _tasks[event_id]
