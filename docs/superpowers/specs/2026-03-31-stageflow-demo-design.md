# StageFlow Demo — Design Spec

## Overview

StageFlow is a network-aware event orchestration platform built on Nokia Network APIs. This spec covers the demo application to be shown to Nokia and T-Mobile representatives. The demo must be deployed to the cloud (Railway) and presented live on a call.

## Goals

- Demonstrate three flows: Priority QoD (real logic), Emergency SOS (real logic), Crowd Control (faked visuals)
- Support switching between Nokia API mocks and real API calls via env var
- Two pre-seeded events: music festival and football match
- One scripted simulation scenario that walks through the full happy path

## Non-Goals

- Authentication, authorization, user management
- Real Nokia Location/Geofencing API integration (simulated locally)
- Native mobile apps
- Production-grade error handling, monitoring, logging
- AI agent (rule-based logic with AI-style UI presentation)

---

## Demo Scenario

### Pre-seeded Data

Two events with zones, staff, and visitors pre-populated via seed script.

### Live Demo Flow (Primeweaver Sound, 2-3 minutes)

1. Open organizer dashboard — map with zones, staff markers
2. Press "Start Simulation" — staff and visitors begin moving on scripted paths
3. Security guard enters Main Stage A zone — QoD boost activated automatically, marker changes color, event log shows "QoD session created"
4. VIP user enters VIP Area — receives 15-minute boost with visible timer
5. Switch to staff mobile view — shows "Priority Network: Active"
6. Security guard exits zone — QoD deactivated automatically
7. Zone Main Stage A turns red — "Crowd density: CRITICAL" (faked). Event log: "AI Alert: Main Stage A overcrowded"
8. Presenter opens visitor mobile view, presses SOS — system finds nearest medic, gives QoD boost, shows incident + route on dashboard
9. Switch event to World Cup 2026 — map redraws with stadium zones, different staff. Shows platform is not hardcoded to one event.

---

## Architecture

### Monorepo Structure

```
hackathon_2026/
├── frontend/          # React + Vite + TypeScript
├── backend/           # Python FastAPI
├── docker-compose.yml # Local dev: backend + frontend + postgres
└── docs/
```

### Services

| Service | Tech | Deploy |
|---------|------|--------|
| Backend | FastAPI, SQLAlchemy, asyncio | Railway (Docker) |
| Frontend | React, Vite, Leaflet, Tailwind CSS | Railway (Nginx + static) |
| Database | PostgreSQL + PostGIS | Railway plugin |

### Communication

- Frontend -> Backend: REST API for CRUD, actions
- Backend -> Frontend: WebSocket for real-time updates (positions, QoD statuses, incidents, crowd levels)

---

## Frontend

### Single React App, Three Views

| Route | User | Purpose |
|-------|------|---------|
| `/dashboard` | Event organizer | Map, zones, staff, event log, crowd density, incidents, event selector, simulation controls |
| `/staff` | Staff / Medic | Own QoD status, zone, role. Medics see SOS alerts |
| `/visitor` | VIP / Regular visitor | QoD boost status, SOS button |

### Key Components

- **EventMap** — Leaflet + OpenStreetMap. Zones as GeoJSON polygons with color coding. Staff/visitor markers that move in real-time via WebSocket.
- **StaffPanel** — List of staff with name, role, QoD status badge
- **CrowdOverlay** — Zone fill color based on crowd_level (green/yellow/orange/red)
- **EventLog** — Scrolling feed of events: QoD activations, zone entries/exits, AI alerts, incidents
- **EventSelector** — Dropdown to switch between Primeweaver Sound and World Cup
- **SosButton** — Red emergency button on visitor view
- **QodBadge** — "Priority Active" / "Normal" indicator

### Styling

Tailwind CSS. No UI framework. Responsive — `/staff` and `/visitor` optimized for mobile viewport.

---

## Backend

### Directory Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, WebSocket
│   ├── config.py            # Settings, NOKIA_MODE switch
│   ├── models/
│   │   ├── event.py         # Event, Zone
│   │   ├── staff.py         # Staff
│   │   ├── visitor.py       # Visitor
│   │   └── incident.py      # Incident
│   ├── api/
│   │   ├── events.py        # CRUD events and zones
│   │   ├── staff.py         # CRUD staff
│   │   ├── simulation.py    # Start/stop/tick
│   │   ├── emergency.py     # SOS trigger
│   │   └── ws.py            # WebSocket endpoint
│   ├── services/
│   │   ├── simulation.py    # Engine: moves entities, checks geofences
│   │   ├── geofence.py      # Point-in-polygon (Shapely)
│   │   ├── qod.py           # QoD orchestration logic
│   │   └── emergency.py     # Find nearest medic, boost, notify
│   ├── nokia/
│   │   ├── client.py        # Abstract interface
│   │   ├── real.py          # Real Nokia NaC SDK calls
│   │   └── mock.py          # Mock: logs, returns fake session IDs
│   └── seed.py              # Pre-populate DB with two events
├── requirements.txt
├── Dockerfile
└── alembic/
```

### API Endpoints

```
GET    /api/events                  # List events
GET    /api/events/{id}             # Event detail with zones
GET    /api/events/{id}/staff       # Staff for event
GET    /api/events/{id}/visitors    # Visitors for event
POST   /api/simulation/start/{id}  # Start simulation for event
POST   /api/simulation/stop/{id}   # Stop simulation
POST   /api/emergency/sos          # Trigger SOS {visitor_id, lat, lng}
POST   /api/emergency/{id}/resolve # Resolve incident
WS     /ws/events/{id}             # Real-time updates for event
```

### Simulation Engine

- Triggered by `POST /api/simulation/start/{id}`
- Runs async background task, ticks every 2 seconds
- Each tick:
  1. Move each entity to next waypoint from SimulationPath
  2. Check point-in-polygon for zone enter/exit
  3. On zone enter: call Nokia QoD create (staff = permanent, VIP = 15min)
  4. On zone exit: call Nokia QoD delete
  5. Update crowd_level on timer (faked)
  6. Push all changes via WebSocket

### SOS Flow

Not part of auto-simulation. Triggered manually:

1. Visitor presses SOS → `POST /api/emergency/sos` with coordinates
2. Backend finds nearest staff with role=medical
3. Activates QoD boost for medic
4. Creates Incident record
5. Pushes to WebSocket: incident marker, medic-to-patient line, alert to medic's staff view

---

## Data Model

### Event
- id, name, description, city, country
- bounds (GeoJSON — map viewport rectangle)
- status (active / archived)

### Zone
- id, event_id (FK)
- name, type (stage / food / entrance / exit / medical / vip / general)
- polygon (GeoJSON coordinates)
- crowd_level (low / medium / high / critical)
- color (hex, for map rendering)

### Staff
- id, event_id (FK)
- name, phone, role (security / medical / logistics / operations / comms)
- device_id (for Nokia API)
- qod_status (active / inactive), qod_session_id
- current_lat, current_lng, current_zone_id (FK, nullable)

### Visitor
- id, event_id (FK)
- name, phone, type (vip / regular)
- device_id
- qod_status, qod_session_id
- current_lat, current_lng, current_zone_id (FK, nullable)

### Incident
- id, event_id (FK)
- type (medical_emergency)
- status (open / responding / resolved)
- reporter_id (visitor FK), responder_id (staff FK, nullable)
- lat, lng
- created_at, resolved_at

### SimulationPath
- id, event_id (FK)
- entity_type (staff / visitor), entity_id
- waypoints (JSON: [{lat, lng, timestamp_offset}])

---

## Nokia API Integration

### Interface

```python
class NokiaClient:
    async def create_qod_session(device_id, profile, duration) -> session_id
    async def delete_qod_session(session_id) -> bool
    async def get_device_location(device_id) -> (lat, lng)       # future
    async def verify_location(device_id, lat, lng, radius) -> bool  # future
```

### Mock Implementation

- `create_qod_session` — logs call, returns `fake-session-{uuid}`, writes to event log. 200-500ms artificial delay.
- `delete_qod_session` — logs, returns True

### Real Implementation

- Uses Nokia Network as Code Python SDK
- Credentials from env: `NOKIA_API_KEY`, `NOKIA_API_SECRET`
- QoD profiles: staff = `QOS_L` (persistent priority), VIP = `QOS_M` (15 minutes)

### Switching

```
NOKIA_MODE=mock   # or real
```

---

## Seed Data

### Event 1: Primeweaver Sound 2026 (Barcelona, Fira Barcelona)

**Zones (12):**
Main Stage A, Main Stage B, Medium Stage 1-5, Food Court, Entrance Gate, Exit Gate, VIP Area, Medical Tent

**Staff (5-6):**

| Name | Role | Simulation Path |
|------|------|----------------|
| Juan Garcia | Security | Outside → enters Main Stage A → patrols → exits |
| Dr. Maria Lopez | Medical | Stationed at Medical Tent |
| Carlos Ruiz | Logistics | Moves between Medium Stages 1-3 |
| Elena Torres | Operations | Entrance Gate area |
| Pedro Sanchez | Comms | Roams between stages |

**Visitors (2):**

| Name | Type | Simulation Path |
|------|------|----------------|
| Anna Berg | VIP | Entrance → VIP Area (15-min boost) → Food Court |
| Visitor X | Regular | Stationary near Main Stage A (SOS trigger) |

### Event 2: World Cup 2026 (Mexico City, Estadio Azteca)

**Zones (10):**
North Stand, South Stand, East Stand, West Stand, VIP Box, Pitch Perimeter, Entrance Gate Norte, Entrance Gate Sur, Medical Point, Media Zone

**Staff (4-5):**
Security, medical, operations roles distributed across zones.

**Visitors (1-2):**
VIP in VIP Box, regular in North Stand.

---

## Deployment

### Railway

- One Railway project, three services from monorepo
- `backend/` — FastAPI Docker container
- `frontend/` — Nginx serving Vite build, proxies `/api/*` and `/ws/*` to backend
- PostgreSQL + PostGIS — Railway plugin
- Backend runs `seed.py` on startup to populate data

### Local Development

```
docker-compose up
```

Starts backend (FastAPI with hot reload), frontend (Vite dev server), and PostgreSQL.

### Environment Variables

```
DATABASE_URL=postgresql://...
NOKIA_MODE=mock
NOKIA_API_KEY=         # when available
NOKIA_API_SECRET=      # when available
```

---

## Team Split

| Who | Focus | Responsibilities |
|-----|-------|-----------------|
| Evgenii | Backend | Models, API endpoints, simulation engine, Nokia client (mock/real), WebSocket, seed data |
| Marc | Frontend | React app, Leaflet map, dashboard, staff/visitor views, WebSocket subscription, styling |
| Ilia | Infra + Integration | Docker, docker-compose, Railway deploy, API contract definition, integration testing, QA |

### Coordination

1. First: agree on API contract (endpoint signatures, request/response shapes) so frontend and backend can work in parallel
2. Parallel: backend + frontend + infra
3. Integration: connect, run through demo scenario, polish
