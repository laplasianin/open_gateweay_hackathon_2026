# StageFlow

Network-Aware Event Orchestration Platform. Built on Nokia Network APIs.

Demo for Nokia / T-Mobile — manages priority network access for staff and VIP at mass events, tracks crowd density, coordinates emergency medical response.

## What's Built

### Backend (Python / FastAPI)

- **REST API** — events, zones, staff, visitors, incidents
- **WebSocket** — real-time updates (positions, QoD statuses, crowd levels, incidents)
- **Simulation Engine** — moves staff/visitors along scripted paths, triggers QoD on zone enter/exit, fakes crowd density
- **Nokia QoD Integration** — mock client (returns fake sessions) + real client stub (plug in API keys when available)
- **Emergency SOS** — finds nearest medic, activates QoD boost, broadcasts incident
- **Seed Data** — two pre-populated events with zones, staff, visitors, and movement paths

### Frontend (React / TypeScript / Vite)

- **Dashboard** (`/dashboard`) — Leaflet map with colored zones, moving staff/visitor markers, staff panel with QoD badges, scrolling event log, simulation controls, event selector
- **Staff View** (`/staff`) — mobile-optimized view showing network status, role, emergency alerts
- **Visitor View** (`/visitor`) — mobile-optimized view with QoD boost status and SOS button

### Infrastructure

- Docker Compose for local dev (PostgreSQL + backend + frontend)
- Dockerfiles for Railway deployment
- Nginx reverse proxy for /api and /ws

## Pre-seeded Events

| Event | Location | Zones | Staff | Visitors |
|-------|----------|-------|-------|----------|
| Primeweaver Sound 2026 | Barcelona, Fira Barcelona | 12 (2 main stages, 5 medium, food court, entrance, exit, VIP, medical) | 5 (security, medical, logistics, operations, comms) | 2 (VIP + regular) |
| World Cup 2026 | Mexico City, Estadio Azteca | 10 (4 stands, VIP box, pitch perimeter, 2 entrances, medical, media) | 4 (security, medical, operations, comms) | 2 (VIP + regular) |

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for frontend dev)
- Python 3.12+ (for backend dev)

### Run with Docker (recommended)

```bash
docker-compose up --build
```

This starts:
- PostgreSQL + PostGIS on port 5432
- Backend (FastAPI) on port 8000
- Frontend (Nginx) on port 3000

Open http://localhost:3000 — the dashboard loads with pre-seeded data.

### Run without Docker (development)

**Terminal 1 — Database:**
```bash
docker run -d --name stageflow-db \
  -e POSTGRES_USER=stageflow \
  -e POSTGRES_PASSWORD=stageflow \
  -e POSTGRES_DB=stageflow \
  -p 5432:5432 \
  postgis/postgis:16-3.4
```

**Terminal 2 — Backend:**
```bash
cd backend
pip install -r requirements.txt
DATABASE_URL=postgresql+asyncpg://stageflow:stageflow@localhost:5432/stageflow \
  uvicorn app.main:app --reload --port 8000
```

**Terminal 3 — Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## How to Test the Demo

### 1. Dashboard

1. Open http://localhost:3000
2. The Primeweaver Sound 2026 event is selected by default
3. You see a map of Barcelona with 12 colored zones
4. Staff panel on the right shows 5 staff members + 2 visitors, all "Normal"

### 2. Start Simulation

1. Click **"Start Simulation"**
2. Watch markers move on the map every 2 seconds
3. Event log fills with entries:
   - "QoD activated for Juan Garcia (entered Main Stage A)"
   - "QoD activated for Anna Berg (entered VIP Area)"
4. Staff panel badges change to "Priority Active" (green)
5. When staff exits a zone, QoD is deactivated automatically

### 3. Crowd Density (faked)

- At ~30 seconds: Main Stage A turns orange ("HIGH")
- At ~45 seconds: Main Stage A turns red ("CRITICAL")
- Event log shows: "AI Alert: Main Stage A crowd density CRITICAL"

### 4. SOS Emergency

1. Open a new tab: http://localhost:3000/visitor?event=EVENT_ID&id=VISITOR_ID
   (Get IDs from the API: http://localhost:8000/api/events then /api/events/{id}/visitors)
2. Press the red **"SOS Emergency"** button
3. On the dashboard:
   - Red SOS marker appears on the map
   - Dashed line from medic to patient
   - Event log: "SOS received! Nearest medic dispatched (Xm away)"
4. Medic gets QoD boost automatically

### 5. Staff Mobile View

1. Open http://localhost:3000/staff?event=EVENT_ID&id=STAFF_ID
2. Shows staff name, role, and network status
3. Updates in real-time via WebSocket — "Priority Active" when in zone
4. Medics see emergency alert when SOS is triggered

### 6. Switch Event

1. Use the dropdown in the top bar to switch to "World Cup 2026"
2. Map redraws with Estadio Azteca zones in Mexico City
3. Different staff and zones — same platform

## API Endpoints

```
GET  /api/health                    — Health check
GET  /api/events                    — List all events
GET  /api/events/{id}               — Event detail with zones
GET  /api/events/{id}/staff         — Staff for event
GET  /api/events/{id}/visitors      — Visitors for event
POST /api/simulation/start/{id}     — Start simulation
POST /api/simulation/stop/{id}      — Stop simulation
POST /api/emergency/sos             — Trigger SOS {visitor_id, lat, lng}
POST /api/emergency/{id}/resolve    — Resolve incident
WS   /ws/events/{id}                — Real-time updates
```

## Nokia API Mode

Controlled by environment variable:

```bash
NOKIA_MODE=mock    # Default. Returns fake session IDs, logs calls.
NOKIA_MODE=real    # Uses Nokia Network as Code SDK. Requires API keys.
```

When Nokia provides API credentials, set:
```bash
NOKIA_MODE=real
NOKIA_API_KEY=your-key
NOKIA_API_SECRET=your-secret
```

No code changes needed — just environment variables.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, asyncio, Shapely |
| Frontend | React 18, TypeScript, Vite, Leaflet, Tailwind CSS |
| Database | PostgreSQL 16 + PostGIS |
| Infrastructure | Docker, Docker Compose, Nginx |
| Deployment | Railway |

## Project Structure

```
hackathon_2026/
├── backend/
│   ├── app/
│   │   ├── api/          # REST + WebSocket endpoints
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Business logic (simulation, geofence, emergency, QoD)
│   │   ├── nokia/        # Nokia API client (mock + real)
│   │   ├── main.py       # FastAPI app
│   │   ├── config.py     # Settings
│   │   ├── database.py   # DB connection
│   │   └── seed.py       # Pre-populate demo data
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # REST client
│   │   ├── hooks/        # useWebSocket, useEvents
│   │   ├── components/   # QodBadge, SosButton
│   │   ├── pages/
│   │   │   ├── Dashboard/  # Map, panels, controls
│   │   │   ├── Staff/      # Mobile staff view
│   │   │   └── Visitor/    # Mobile visitor view
│   │   └── types/        # TypeScript interfaces
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
└── docs/
    ├── deployment.md
    └── stageflow-demo-flows-ru.md
```

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

Tests cover: geofence (point-in-polygon), Nokia mock client, emergency (nearest medic), simulation (waypoint interpolation).
