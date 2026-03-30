"""Seed database with two demo events, zones, staff, visitors, and simulation paths."""

from sqlalchemy import select
from app.database import async_session, engine, Base
from app.models.event import Event, Zone
from app.models.staff import Staff
from app.models.visitor import Visitor
from app.models.simulation_path import SimulationPath


PRIMEWEAVER_BOUNDS = {"north": 41.360, "south": 41.349, "east": 2.135, "west": 2.122}

PRIMEWEAVER_ZONES = [
    {"name": "Main Stage A", "type": "stage", "color": "#EF4444",
     "polygon": [[2.1240, 41.3555], [2.1260, 41.3555], [2.1260, 41.3565], [2.1240, 41.3565], [2.1240, 41.3555]]},
    {"name": "Main Stage B", "type": "stage", "color": "#F97316",
     "polygon": [[2.1270, 41.3555], [2.1290, 41.3555], [2.1290, 41.3565], [2.1270, 41.3565], [2.1270, 41.3555]]},
    {"name": "Medium Stage 1", "type": "stage", "color": "#8B5CF6",
     "polygon": [[2.1240, 41.3535], [2.1252, 41.3535], [2.1252, 41.3545], [2.1240, 41.3545], [2.1240, 41.3535]]},
    {"name": "Medium Stage 2", "type": "stage", "color": "#8B5CF6",
     "polygon": [[2.1258, 41.3535], [2.1270, 41.3535], [2.1270, 41.3545], [2.1258, 41.3545], [2.1258, 41.3535]]},
    {"name": "Medium Stage 3", "type": "stage", "color": "#8B5CF6",
     "polygon": [[2.1276, 41.3535], [2.1288, 41.3535], [2.1288, 41.3545], [2.1276, 41.3545], [2.1276, 41.3535]]},
    {"name": "Medium Stage 4", "type": "stage", "color": "#8B5CF6",
     "polygon": [[2.1294, 41.3535], [2.1306, 41.3535], [2.1306, 41.3545], [2.1294, 41.3545], [2.1294, 41.3535]]},
    {"name": "Medium Stage 5", "type": "stage", "color": "#8B5CF6",
     "polygon": [[2.1240, 41.3520], [2.1252, 41.3520], [2.1252, 41.3530], [2.1240, 41.3530], [2.1240, 41.3520]]},
    {"name": "Food Court", "type": "food", "color": "#F59E0B",
     "polygon": [[2.1300, 41.3555], [2.1320, 41.3555], [2.1320, 41.3565], [2.1300, 41.3565], [2.1300, 41.3555]]},
    {"name": "Entrance Gate", "type": "entrance", "color": "#10B981",
     "polygon": [[2.1230, 41.3500], [2.1245, 41.3500], [2.1245, 41.3510], [2.1230, 41.3510], [2.1230, 41.3500]]},
    {"name": "Exit Gate", "type": "exit", "color": "#6B7280",
     "polygon": [[2.1310, 41.3500], [2.1325, 41.3500], [2.1325, 41.3510], [2.1310, 41.3510], [2.1310, 41.3500]]},
    {"name": "VIP Area", "type": "vip", "color": "#EC4899",
     "polygon": [[2.1295, 41.3560], [2.1315, 41.3560], [2.1315, 41.3572], [2.1295, 41.3572], [2.1295, 41.3560]]},
    {"name": "Medical Tent", "type": "medical", "color": "#14B8A6",
     "polygon": [[2.1258, 41.3505], [2.1272, 41.3505], [2.1272, 41.3515], [2.1258, 41.3515], [2.1258, 41.3505]]},
]

PRIMEWEAVER_STAFF = [
    {"name": "Juan Garcia", "phone": "+34 600 111 222", "role": "security", "device_id": "dev-juan-001"},
    {"name": "Dr. Maria Lopez", "phone": "+34 600 333 444", "role": "medical", "device_id": "dev-maria-002"},
    {"name": "Carlos Ruiz", "phone": "+34 600 555 666", "role": "logistics", "device_id": "dev-carlos-003"},
    {"name": "Elena Torres", "phone": "+34 600 777 888", "role": "operations", "device_id": "dev-elena-004"},
    {"name": "Pedro Sanchez", "phone": "+34 600 999 000", "role": "comms", "device_id": "dev-pedro-005"},
]

PRIMEWEAVER_VISITORS = [
    {"name": "Anna Berg", "phone": "+49 170 123 4567", "type": "vip", "device_id": "dev-anna-v01"},
    {"name": "Visitor X", "phone": "+34 611 000 111", "type": "regular", "device_id": "dev-visitor-v02"},
]

PRIMEWEAVER_STAFF_PATHS = {
    "Juan Garcia": [
        {"lat": 41.3495, "lng": 2.1240, "offset": 0},
        {"lat": 41.3510, "lng": 2.1242, "offset": 10},
        {"lat": 41.3558, "lng": 2.1250, "offset": 20},
        {"lat": 41.3560, "lng": 2.1255, "offset": 40},
        {"lat": 41.3558, "lng": 2.1250, "offset": 50},
        {"lat": 41.3548, "lng": 2.1250, "offset": 60},
        {"lat": 41.3530, "lng": 2.1250, "offset": 70},
    ],
    "Dr. Maria Lopez": [
        {"lat": 41.3510, "lng": 2.1265, "offset": 0},
        {"lat": 41.3510, "lng": 2.1265, "offset": 120},
    ],
    "Carlos Ruiz": [
        {"lat": 41.3540, "lng": 2.1245, "offset": 0},
        {"lat": 41.3540, "lng": 2.1264, "offset": 15},
        {"lat": 41.3540, "lng": 2.1282, "offset": 30},
        {"lat": 41.3540, "lng": 2.1264, "offset": 45},
        {"lat": 41.3540, "lng": 2.1245, "offset": 60},
    ],
    "Elena Torres": [
        {"lat": 41.3505, "lng": 2.1237, "offset": 0},
        {"lat": 41.3505, "lng": 2.1237, "offset": 120},
    ],
    "Pedro Sanchez": [
        {"lat": 41.3560, "lng": 2.1245, "offset": 0},
        {"lat": 41.3560, "lng": 2.1280, "offset": 20},
        {"lat": 41.3560, "lng": 2.1310, "offset": 40},
        {"lat": 41.3560, "lng": 2.1280, "offset": 60},
        {"lat": 41.3560, "lng": 2.1245, "offset": 80},
    ],
}

PRIMEWEAVER_VISITOR_PATHS = {
    "Anna Berg": [
        {"lat": 41.3505, "lng": 2.1237, "offset": 0},
        {"lat": 41.3530, "lng": 2.1270, "offset": 15},
        {"lat": 41.3565, "lng": 2.1305, "offset": 25},
        {"lat": 41.3566, "lng": 2.1308, "offset": 55},
        {"lat": 41.3560, "lng": 2.1310, "offset": 70},
    ],
    "Visitor X": [
        {"lat": 41.3552, "lng": 2.1248, "offset": 0},
        {"lat": 41.3552, "lng": 2.1248, "offset": 120},
    ],
}


WORLDCUP_BOUNDS = {"north": 19.306, "south": 19.300, "east": -99.147, "west": -99.154}

WORLDCUP_ZONES = [
    {"name": "North Stand", "type": "general", "color": "#3B82F6",
     "polygon": [[-99.1520, 19.3040], [-99.1490, 19.3040], [-99.1490, 19.3048], [-99.1520, 19.3048], [-99.1520, 19.3040]]},
    {"name": "South Stand", "type": "general", "color": "#3B82F6",
     "polygon": [[-99.1520, 19.3012], [-99.1490, 19.3012], [-99.1490, 19.3020], [-99.1520, 19.3020], [-99.1520, 19.3012]]},
    {"name": "East Stand", "type": "general", "color": "#3B82F6",
     "polygon": [[-99.1490, 19.3020], [-99.1482, 19.3020], [-99.1482, 19.3040], [-99.1490, 19.3040], [-99.1490, 19.3020]]},
    {"name": "West Stand", "type": "general", "color": "#3B82F6",
     "polygon": [[-99.1520, 19.3020], [-99.1528, 19.3020], [-99.1528, 19.3040], [-99.1520, 19.3040], [-99.1520, 19.3020]]},
    {"name": "VIP Box", "type": "vip", "color": "#EC4899",
     "polygon": [[-99.1528, 19.3028], [-99.1535, 19.3028], [-99.1535, 19.3035], [-99.1528, 19.3035], [-99.1528, 19.3028]]},
    {"name": "Pitch Perimeter", "type": "general", "color": "#10B981",
     "polygon": [[-99.1518, 19.3022], [-99.1492, 19.3022], [-99.1492, 19.3038], [-99.1518, 19.3038], [-99.1518, 19.3022]]},
    {"name": "Entrance Gate Norte", "type": "entrance", "color": "#10B981",
     "polygon": [[-99.1510, 19.3050], [-99.1500, 19.3050], [-99.1500, 19.3055], [-99.1510, 19.3055], [-99.1510, 19.3050]]},
    {"name": "Entrance Gate Sur", "type": "entrance", "color": "#10B981",
     "polygon": [[-99.1510, 19.3005], [-99.1500, 19.3005], [-99.1500, 19.3010], [-99.1510, 19.3010], [-99.1510, 19.3005]]},
    {"name": "Medical Point", "type": "medical", "color": "#14B8A6",
     "polygon": [[-99.1500, 19.3048], [-99.1492, 19.3048], [-99.1492, 19.3053], [-99.1500, 19.3053], [-99.1500, 19.3048]]},
    {"name": "Media Zone", "type": "general", "color": "#A855F7",
     "polygon": [[-99.1492, 19.3012], [-99.1482, 19.3012], [-99.1482, 19.3018], [-99.1492, 19.3018], [-99.1492, 19.3012]]},
]

WORLDCUP_STAFF = [
    {"name": "Miguel Hernandez", "phone": "+52 55 1234 5678", "role": "security", "device_id": "dev-miguel-001"},
    {"name": "Dr. Sofia Reyes", "phone": "+52 55 2345 6789", "role": "medical", "device_id": "dev-sofia-002"},
    {"name": "Luis Morales", "phone": "+52 55 3456 7890", "role": "operations", "device_id": "dev-luis-003"},
    {"name": "Ana Gutierrez", "phone": "+52 55 4567 8901", "role": "comms", "device_id": "dev-ana-004"},
]

WORLDCUP_VISITORS = [
    {"name": "James Wilson", "phone": "+1 555 0123", "type": "vip", "device_id": "dev-james-v01"},
    {"name": "Fan Y", "phone": "+52 55 9999 0000", "type": "regular", "device_id": "dev-fan-v02"},
]

WORLDCUP_STAFF_PATHS = {
    "Miguel Hernandez": [
        {"lat": 19.3044, "lng": -99.1505, "offset": 0},
        {"lat": 19.3044, "lng": -99.1505, "offset": 120},
    ],
    "Dr. Sofia Reyes": [
        {"lat": 19.3050, "lng": -99.1496, "offset": 0},
        {"lat": 19.3050, "lng": -99.1496, "offset": 120},
    ],
    "Luis Morales": [
        {"lat": 19.3008, "lng": -99.1505, "offset": 0},
        {"lat": 19.3030, "lng": -99.1505, "offset": 30},
        {"lat": 19.3050, "lng": -99.1505, "offset": 60},
    ],
    "Ana Gutierrez": [
        {"lat": 19.3030, "lng": -99.1510, "offset": 0},
        {"lat": 19.3030, "lng": -99.1510, "offset": 120},
    ],
}

WORLDCUP_VISITOR_PATHS = {
    "James Wilson": [
        {"lat": 19.3052, "lng": -99.1505, "offset": 0},
        {"lat": 19.3032, "lng": -99.1531, "offset": 20},
        {"lat": 19.3032, "lng": -99.1531, "offset": 120},
    ],
    "Fan Y": [
        {"lat": 19.3044, "lng": -99.1505, "offset": 0},
        {"lat": 19.3044, "lng": -99.1505, "offset": 120},
    ],
}


async def seed_if_empty():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        result = await db.execute(select(Event))
        if result.scalars().first() is not None:
            return

        await _seed_event(
            db,
            name="Primeweaver Sound 2026",
            description="Electronic music festival in Barcelona",
            city="Barcelona",
            country="Spain",
            bounds=PRIMEWEAVER_BOUNDS,
            zones=PRIMEWEAVER_ZONES,
            staff=PRIMEWEAVER_STAFF,
            visitors=PRIMEWEAVER_VISITORS,
            staff_paths=PRIMEWEAVER_STAFF_PATHS,
            visitor_paths=PRIMEWEAVER_VISITOR_PATHS,
        )

        await _seed_event(
            db,
            name="World Cup 2026",
            description="FIFA World Cup match at Estadio Azteca",
            city="Mexico City",
            country="Mexico",
            bounds=WORLDCUP_BOUNDS,
            zones=WORLDCUP_ZONES,
            staff=WORLDCUP_STAFF,
            visitors=WORLDCUP_VISITORS,
            staff_paths=WORLDCUP_STAFF_PATHS,
            visitor_paths=WORLDCUP_VISITOR_PATHS,
        )

        await db.commit()


async def _seed_event(db, *, name, description, city, country, bounds, zones, staff, visitors, staff_paths, visitor_paths):
    event = Event(name=name, description=description, city=city, country=country, bounds=bounds)
    db.add(event)
    await db.flush()

    for z in zones:
        zone = Zone(event_id=event.id, name=z["name"], type=z.get("type", "general"), polygon=z["polygon"], color=z.get("color", "#3B82F6"))
        db.add(zone)
    await db.flush()

    staff_map = {}
    for s in staff:
        obj = Staff(event_id=event.id, name=s["name"], phone=s["phone"], role=s["role"], device_id=s["device_id"])
        db.add(obj)
        staff_map[s["name"]] = obj
    await db.flush()

    visitor_map = {}
    for v in visitors:
        obj = Visitor(event_id=event.id, name=v["name"], phone=v["phone"], type=v["type"], device_id=v["device_id"])
        db.add(obj)
        visitor_map[v["name"]] = obj
    await db.flush()

    for name_key, waypoints in staff_paths.items():
        if name_key in staff_map:
            path = SimulationPath(event_id=event.id, entity_type="staff", entity_id=staff_map[name_key].id, waypoints=waypoints)
            db.add(path)

    for name_key, waypoints in visitor_paths.items():
        if name_key in visitor_map:
            path = SimulationPath(event_id=event.id, entity_type="visitor", entity_id=visitor_map[name_key].id, waypoints=waypoints)
            db.add(path)
