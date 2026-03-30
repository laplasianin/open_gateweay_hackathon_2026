# StageFlow Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deployable demo of StageFlow — a network-aware event orchestration platform — showing QoD priority for staff/VIP, emergency SOS flow, and faked crowd density, all on a real-time map dashboard.

**Architecture:** Monorepo with FastAPI backend (Python), React+Vite frontend (TypeScript), and PostgreSQL+PostGIS. Backend runs simulation engine that moves entities along scripted paths, triggers Nokia QoD API (mock or real), and pushes updates to frontend via WebSocket. Frontend renders Leaflet map with zones, moving markers, and event log.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0, asyncio, Shapely, Alembic | React 18, Vite, TypeScript, Leaflet, Tailwind CSS | PostgreSQL 16 + PostGIS | Docker, docker-compose | Railway

---

## File Structure

### Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app, CORS, lifespan, include routers
│   ├── config.py                  # Pydantic Settings: DATABASE_URL, NOKIA_MODE, etc.
│   ├── database.py                # SQLAlchemy engine, async session factory
│   ├── models/
│   │   ├── __init__.py            # Import all models for Alembic
│   │   ├── event.py               # Event, Zone models
│   │   ├── staff.py               # Staff model
│   │   ├── visitor.py             # Visitor model
│   │   ├── incident.py            # Incident model
│   │   └── simulation_path.py     # SimulationPath model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── event.py               # Pydantic schemas for Event, Zone
│   │   ├── staff.py               # Pydantic schemas for Staff
│   │   ├── visitor.py             # Pydantic schemas for Visitor
│   │   ├── incident.py            # Pydantic schemas for Incident
│   │   └── ws.py                  # WebSocket message schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── events.py              # GET /api/events, GET /api/events/{id}
│   │   ├── staff.py               # GET /api/events/{id}/staff
│   │   ├── visitors.py            # GET /api/events/{id}/visitors
│   │   ├── simulation.py          # POST /api/simulation/start/{id}, stop/{id}
│   │   ├── emergency.py           # POST /api/emergency/sos, /api/emergency/{id}/resolve
│   │   └── ws.py                  # WS /ws/events/{id}
│   ├── services/
│   │   ├── __init__.py
│   │   ├── simulation.py          # SimulationEngine: tick loop, move entities, check zones
│   │   ├── geofence.py            # point_in_polygon(), check zone enter/exit
│   │   ├── qod.py                 # QoD orchestration: activate/deactivate based on role
│   │   ├── emergency.py           # find_nearest_medic(), handle SOS
│   │   └── ws_manager.py          # WebSocket connection manager, broadcast
│   ├── nokia/
│   │   ├── __init__.py
│   │   ├── base.py                # NokiaClient ABC
│   │   ├── mock.py                # MockNokiaClient
│   │   └── real.py                # RealNokiaClient (Nokia NaC SDK)
│   └── seed.py                    # Seed DB with two events, zones, staff, visitors, paths
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Fixtures: test DB, async client, seed data
│   ├── test_geofence.py           # Point-in-polygon tests
│   ├── test_nokia_mock.py         # Mock Nokia client tests
│   ├── test_qod_service.py        # QoD orchestration tests
│   ├── test_emergency.py          # Emergency flow tests
│   ├── test_simulation.py         # Simulation engine tests
│   └── test_api.py                # API endpoint integration tests
├── alembic/
│   ├── env.py
│   └── versions/                  # Migration files
├── alembic.ini
├── requirements.txt
├── Dockerfile
└── .env.example
```

### Frontend

```
frontend/
├── src/
│   ├── App.tsx                     # React Router: /dashboard, /staff, /visitor
│   ├── main.tsx                    # Entry point
│   ├── api/
│   │   └── client.ts              # Fetch wrapper for REST + WebSocket hook
│   ├── hooks/
│   │   ├── useWebSocket.ts        # Connect to WS, parse messages, update state
│   │   └── useEvents.ts           # Fetch events list
│   ├── types/
│   │   └── index.ts               # TypeScript types matching backend schemas
│   ├── pages/
│   │   ├── Dashboard/
│   │   │   ├── DashboardPage.tsx   # Layout: map + side panels
│   │   │   ├── EventMap.tsx        # Leaflet map, zones, markers
│   │   │   ├── ZonePolygon.tsx     # Single zone polygon with color
│   │   │   ├── EntityMarker.tsx    # Staff/visitor marker with icon + tooltip
│   │   │   ├── IncidentMarker.tsx  # SOS marker + line to medic
│   │   │   ├── StaffPanel.tsx      # Staff list with QoD badges
│   │   │   ├── EventLog.tsx        # Scrolling event feed
│   │   │   ├── EventSelector.tsx   # Event dropdown
│   │   │   └── SimControls.tsx     # Start/Stop simulation buttons
│   │   ├── Staff/
│   │   │   └── StaffPage.tsx       # Mobile: status, zone, alerts
│   │   └── Visitor/
│   │       └── VisitorPage.tsx     # Mobile: QoD status, SOS button
│   └── components/
│       ├── QodBadge.tsx            # "Priority Active" / "Normal" badge
│       └── SosButton.tsx           # Red emergency button
├── public/
│   └── markers/                    # SVG icons for map markers
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── Dockerfile
├── nginx.conf                     # Proxy /api and /ws to backend
└── .env.example
```

### Root

```
hackathon_2026/
├── docker-compose.yml
├── .env.example
├── frontend/
├── backend/
└── docs/
```

---

## Task 1: Project Scaffold & Docker Setup

**Files:**
- Create: `docker-compose.yml`
- Create: `.env.example`
- Create: `backend/requirements.txt`
- Create: `backend/Dockerfile`
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`
- Create: `backend/app/config.py`
- Create: `frontend/package.json` (via npm create vite)
- Create: `frontend/Dockerfile`
- Create: `frontend/nginx.conf`

- [ ] **Step 1: Create backend skeleton**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026
mkdir -p backend/app backend/tests backend/alembic/versions
touch backend/app/__init__.py backend/tests/__init__.py
```

- [ ] **Step 2: Write backend requirements.txt**

Create `backend/requirements.txt`:
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0
alembic==1.14.0
geoalchemy2==0.15.2
shapely==2.0.6
pydantic-settings==2.6.0
httpx==0.28.0
network-as-code==0.3.0
pytest==8.3.0
pytest-asyncio==0.24.0
```

- [ ] **Step 3: Write backend config.py**

Create `backend/app/config.py`:
```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://stageflow:stageflow@localhost:5432/stageflow"
    nokia_mode: str = "mock"  # "mock" or "real"
    nokia_api_key: str = ""
    nokia_api_secret: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
```

- [ ] **Step 4: Write backend main.py**

Create `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StageFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 5: Write backend Dockerfile**

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgeos-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 6: Create React + Vite frontend**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install react-router-dom leaflet react-leaflet @types/leaflet tailwindcss @tailwindcss/vite
```

- [ ] **Step 7: Configure Tailwind**

Replace `frontend/vite.config.ts`:
```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000,
    proxy: {
      "/api": "http://localhost:8000",
      "/ws": { target: "ws://localhost:8000", ws: true },
    },
  },
});
```

Replace `frontend/src/index.css`:
```css
@import "tailwindcss";
```

- [ ] **Step 8: Write minimal App.tsx with router**

Replace `frontend/src/App.tsx`:
```tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";

function Dashboard() {
  return <div className="p-4 text-white bg-gray-900 min-h-screen">Dashboard</div>;
}

function Staff() {
  return <div className="p-4">Staff View</div>;
}

function Visitor() {
  return <div className="p-4">Visitor View</div>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/staff" element={<Staff />} />
        <Route path="/visitor" element={<Visitor />} />
      </Routes>
    </BrowserRouter>
  );
}
```

- [ ] **Step 9: Write frontend Dockerfile and nginx.conf**

Create `frontend/nginx.conf`:
```nginx
server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

Create `frontend/Dockerfile`:
```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

- [ ] **Step 10: Write docker-compose.yml**

Create `docker-compose.yml` at repo root:
```yaml
services:
  postgres:
    image: postgis/postgis:16-3.4
    environment:
      POSTGRES_USER: stageflow
      POSTGRES_PASSWORD: stageflow
      POSTGRES_DB: stageflow
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://stageflow:stageflow@postgres:5432/stageflow
      NOKIA_MODE: mock
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  pgdata:
```

- [ ] **Step 11: Write .env.example**

Create `.env.example` at repo root:
```
DATABASE_URL=postgresql+asyncpg://stageflow:stageflow@localhost:5432/stageflow
NOKIA_MODE=mock
NOKIA_API_KEY=
NOKIA_API_SECRET=
```

- [ ] **Step 12: Verify everything starts**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026
docker-compose up --build
```

Expected: postgres starts, backend responds at `http://localhost:8000/api/health` with `{"status": "ok"}`, frontend shows "Dashboard" at `http://localhost:3000`.

- [ ] **Step 13: Commit**

```bash
git add -A
git commit -m "feat: project scaffold with FastAPI, React+Vite, Docker"
```

---

## Task 2: Database Models & Migrations

**Files:**
- Create: `backend/app/database.py`
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/event.py`
- Create: `backend/app/models/staff.py`
- Create: `backend/app/models/visitor.py`
- Create: `backend/app/models/incident.py`
- Create: `backend/app/models/simulation_path.py`
- Create: `backend/alembic.ini`
- Create: `backend/alembic/env.py`

- [ ] **Step 1: Write database.py**

Create `backend/app/database.py`:
```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session
```

- [ ] **Step 2: Write Event and Zone models**

Create `backend/app/models/event.py`:
```python
import uuid

from geoalchemy2 import Geometry
from sqlalchemy import Column, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    bounds = Column(JSON, nullable=False)  # {"north": float, "south": float, "east": float, "west": float}
    status = Column(String(20), default="active")

    zones = relationship("Zone", back_populates="event", cascade="all, delete-orphan")
    staff = relationship("Staff", back_populates="event", cascade="all, delete-orphan")
    visitors = relationship("Visitor", back_populates="event", cascade="all, delete-orphan")


class Zone(Base):
    __tablename__ = "zones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # stage, food, entrance, exit, medical, vip, general
    polygon = Column(JSON, nullable=False)  # GeoJSON coordinates: [[lng, lat], ...]
    crowd_level = Column(String(20), default="low")  # low, medium, high, critical
    color = Column(String(7), default="#3B82F6")  # hex color

    event = relationship("Event", back_populates="zones")
```

- [ ] **Step 3: Write Staff model**

Create `backend/app/models/staff.py`:
```python
import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)  # security, medical, logistics, operations, comms
    device_id = Column(String(100), default="")
    qod_status = Column(String(20), default="inactive")  # active, inactive
    qod_session_id = Column(String(255), nullable=True)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    current_zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=True)

    event = relationship("Event", back_populates="staff")
    current_zone = relationship("Zone", foreign_keys=[current_zone_id])
```

- [ ] **Step 4: Write Visitor model**

Create `backend/app/models/visitor.py`:
```python
import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)  # vip, regular
    device_id = Column(String(100), default="")
    qod_status = Column(String(20), default="inactive")
    qod_session_id = Column(String(255), nullable=True)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    current_zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=True)

    event = relationship("Event", back_populates="visitors")
    current_zone = relationship("Zone", foreign_keys=[current_zone_id])
```

- [ ] **Step 5: Write Incident model**

Create `backend/app/models/incident.py`:
```python
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    type = Column(String(50), default="medical_emergency")
    status = Column(String(20), default="open")  # open, responding, resolved
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("visitors.id"), nullable=True)
    responder_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime, nullable=True)
```

- [ ] **Step 6: Write SimulationPath model**

Create `backend/app/models/simulation_path.py`:
```python
import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.database import Base


class SimulationPath(Base):
    __tablename__ = "simulation_paths"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    entity_type = Column(String(20), nullable=False)  # "staff" or "visitor"
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    waypoints = Column(JSON, nullable=False)  # [{"lat": float, "lng": float, "offset": int}]
```

- [ ] **Step 7: Write models __init__.py**

Create `backend/app/models/__init__.py`:
```python
from app.models.event import Event, Zone
from app.models.incident import Incident
from app.models.simulation_path import SimulationPath
from app.models.staff import Staff
from app.models.visitor import Visitor

__all__ = ["Event", "Zone", "Staff", "Visitor", "Incident", "SimulationPath"]
```

- [ ] **Step 8: Initialize Alembic**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026/backend
pip install -r requirements.txt
alembic init alembic
```

- [ ] **Step 9: Configure alembic/env.py**

Replace `backend/alembic/env.py`:
```python
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.database import Base
from app.models import *  # noqa: F401, F403 — register all models

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(url=settings.database_url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(settings.database_url)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```

- [ ] **Step 10: Generate and run migration**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026/backend
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

Expected: Tables `events`, `zones`, `staff`, `visitors`, `incidents`, `simulation_paths` created.

- [ ] **Step 11: Commit**

```bash
git add -A
git commit -m "feat: database models and initial migration"
```

---

## Task 3: Pydantic Schemas & API Contract

**Files:**
- Create: `backend/app/schemas/__init__.py`
- Create: `backend/app/schemas/event.py`
- Create: `backend/app/schemas/staff.py`
- Create: `backend/app/schemas/visitor.py`
- Create: `backend/app/schemas/incident.py`
- Create: `backend/app/schemas/ws.py`
- Create: `frontend/src/types/index.ts`

- [ ] **Step 1: Write event schemas**

Create `backend/app/schemas/__init__.py`:
```python
```

Create `backend/app/schemas/event.py`:
```python
from uuid import UUID

from pydantic import BaseModel


class ZoneResponse(BaseModel):
    id: UUID
    name: str
    type: str
    polygon: list[list[float]]  # [[lng, lat], ...]
    crowd_level: str
    color: str

    model_config = {"from_attributes": True}


class EventResponse(BaseModel):
    id: UUID
    name: str
    description: str
    city: str
    country: str
    bounds: dict
    status: str
    zones: list[ZoneResponse] = []

    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    id: UUID
    name: str
    city: str
    country: str
    status: str

    model_config = {"from_attributes": True}
```

- [ ] **Step 2: Write staff schemas**

Create `backend/app/schemas/staff.py`:
```python
from uuid import UUID

from pydantic import BaseModel


class StaffResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    role: str
    device_id: str
    qod_status: str
    qod_session_id: str | None
    current_lat: float | None
    current_lng: float | None
    current_zone_id: UUID | None

    model_config = {"from_attributes": True}
```

- [ ] **Step 3: Write visitor schemas**

Create `backend/app/schemas/visitor.py`:
```python
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
```

- [ ] **Step 4: Write incident schemas**

Create `backend/app/schemas/incident.py`:
```python
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SosRequest(BaseModel):
    visitor_id: UUID
    lat: float
    lng: float


class IncidentResponse(BaseModel):
    id: UUID
    event_id: UUID
    type: str
    status: str
    reporter_id: UUID | None
    responder_id: UUID | None
    lat: float
    lng: float
    created_at: datetime
    resolved_at: datetime | None

    model_config = {"from_attributes": True}
```

- [ ] **Step 5: Write WebSocket message schemas**

Create `backend/app/schemas/ws.py`:
```python
from pydantic import BaseModel


class WsMessage(BaseModel):
    type: str  # "position_update", "qod_update", "zone_update", "incident", "log"
    data: dict
```

- [ ] **Step 6: Write frontend TypeScript types**

Create `frontend/src/types/index.ts`:
```typescript
export interface Event {
  id: string;
  name: string;
  description: string;
  city: string;
  country: string;
  bounds: { north: number; south: number; east: number; west: number };
  status: string;
  zones: Zone[];
}

export interface EventListItem {
  id: string;
  name: string;
  city: string;
  country: string;
  status: string;
}

export interface Zone {
  id: string;
  name: string;
  type: string;
  polygon: [number, number][]; // [lng, lat][]
  crowd_level: "low" | "medium" | "high" | "critical";
  color: string;
}

export interface Staff {
  id: string;
  name: string;
  phone: string;
  role: string;
  device_id: string;
  qod_status: "active" | "inactive";
  qod_session_id: string | null;
  current_lat: number | null;
  current_lng: number | null;
  current_zone_id: string | null;
}

export interface Visitor {
  id: string;
  name: string;
  phone: string;
  type: "vip" | "regular";
  device_id: string;
  qod_status: "active" | "inactive";
  qod_session_id: string | null;
  current_lat: number | null;
  current_lng: number | null;
  current_zone_id: string | null;
}

export interface Incident {
  id: string;
  event_id: string;
  type: string;
  status: "open" | "responding" | "resolved";
  reporter_id: string | null;
  responder_id: string | null;
  lat: number;
  lng: number;
  created_at: string;
  resolved_at: string | null;
}

export interface WsMessage {
  type:
    | "position_update"
    | "qod_update"
    | "zone_update"
    | "incident"
    | "log";
  data: Record<string, unknown>;
}

export interface LogEntry {
  id: string;
  timestamp: string;
  message: string;
  level: "info" | "warning" | "critical" | "success";
}
```

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: Pydantic schemas and TypeScript types (API contract)"
```

---

## Task 4: Nokia Client (Mock + Real Interface)

**Files:**
- Create: `backend/app/nokia/__init__.py`
- Create: `backend/app/nokia/base.py`
- Create: `backend/app/nokia/mock.py`
- Create: `backend/app/nokia/real.py`
- Create: `backend/tests/test_nokia_mock.py`

- [ ] **Step 1: Write failing test for mock Nokia client**

Create `backend/tests/conftest.py`:
```python
import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"
```

Create `backend/tests/test_nokia_mock.py`:
```python
import pytest

from app.nokia.mock import MockNokiaClient


@pytest.mark.anyio
async def test_create_qod_session_returns_session_id():
    client = MockNokiaClient()
    session_id = await client.create_qod_session("device-123", "QOS_L", duration=None)
    assert session_id is not None
    assert session_id.startswith("fake-session-")


@pytest.mark.anyio
async def test_delete_qod_session_returns_true():
    client = MockNokiaClient()
    session_id = await client.create_qod_session("device-123", "QOS_L", duration=None)
    result = await client.delete_qod_session(session_id)
    assert result is True


@pytest.mark.anyio
async def test_create_qod_session_logs_call():
    client = MockNokiaClient()
    await client.create_qod_session("device-456", "QOS_M", duration=900)
    assert len(client.call_log) == 1
    assert client.call_log[0]["action"] == "create_qod_session"
    assert client.call_log[0]["device_id"] == "device-456"
    assert client.call_log[0]["profile"] == "QOS_M"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026/backend
python -m pytest tests/test_nokia_mock.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'app.nokia.mock'`

- [ ] **Step 3: Write Nokia client base and mock**

Create `backend/app/nokia/__init__.py`:
```python
```

Create `backend/app/nokia/base.py`:
```python
from abc import ABC, abstractmethod


class NokiaClient(ABC):
    @abstractmethod
    async def create_qod_session(
        self, device_id: str, profile: str, duration: int | None
    ) -> str:
        """Create QoD session. Returns session_id."""
        ...

    @abstractmethod
    async def delete_qod_session(self, session_id: str) -> bool:
        """Delete QoD session. Returns True on success."""
        ...
```

Create `backend/app/nokia/mock.py`:
```python
import asyncio
import random
import uuid
from datetime import datetime, timezone

from app.nokia.base import NokiaClient


class MockNokiaClient(NokiaClient):
    def __init__(self):
        self.call_log: list[dict] = []
        self._sessions: set[str] = set()

    async def create_qod_session(
        self, device_id: str, profile: str, duration: int | None
    ) -> str:
        await asyncio.sleep(random.uniform(0.2, 0.5))
        session_id = f"fake-session-{uuid.uuid4().hex[:12]}"
        self._sessions.add(session_id)
        self.call_log.append(
            {
                "action": "create_qod_session",
                "device_id": device_id,
                "profile": profile,
                "duration": duration,
                "session_id": session_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        return session_id

    async def delete_qod_session(self, session_id: str) -> bool:
        await asyncio.sleep(random.uniform(0.1, 0.3))
        self._sessions.discard(session_id)
        self.call_log.append(
            {
                "action": "delete_qod_session",
                "session_id": session_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        return True
```

Create `backend/app/nokia/real.py`:
```python
from app.nokia.base import NokiaClient


class RealNokiaClient(NokiaClient):
    """Real Nokia Network as Code SDK integration.

    Requires NOKIA_API_KEY and NOKIA_API_SECRET to be set.
    Will be implemented when Nokia provides API credentials.
    """

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    async def create_qod_session(
        self, device_id: str, profile: str, duration: int | None
    ) -> str:
        raise NotImplementedError("Real Nokia client not yet configured — set NOKIA_MODE=mock")

    async def delete_qod_session(self, session_id: str) -> bool:
        raise NotImplementedError("Real Nokia client not yet configured — set NOKIA_MODE=mock")
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026/backend
python -m pytest tests/test_nokia_mock.py -v
```

Expected: 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: Nokia client abstraction with mock implementation"
```

---

## Task 5: Geofence Service

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/geofence.py`
- Create: `backend/tests/test_geofence.py`

- [ ] **Step 1: Write failing test**

Create `backend/app/services/__init__.py`:
```python
```

Create `backend/tests/test_geofence.py`:
```python
from app.services.geofence import point_in_polygon


def test_point_inside_polygon():
    # Simple square zone
    polygon = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]
    assert point_in_polygon(5.0, 5.0, polygon) is True


def test_point_outside_polygon():
    polygon = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]
    assert point_in_polygon(15.0, 5.0, polygon) is False


def test_point_on_edge():
    polygon = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]
    # On the boundary — Shapely considers this as inside with `contains` or boundary check
    assert point_in_polygon(0.0, 5.0, polygon) is True


def test_find_zone_for_point():
    from app.services.geofence import find_zone

    zones = [
        {"id": "zone-a", "polygon": [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]},
        {"id": "zone-b", "polygon": [[20, 20], [30, 20], [30, 30], [20, 30], [20, 20]]},
    ]
    assert find_zone(5.0, 5.0, zones) == "zone-a"
    assert find_zone(25.0, 25.0, zones) == "zone-b"
    assert find_zone(15.0, 15.0, zones) is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026/backend
python -m pytest tests/test_geofence.py -v
```

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write geofence service**

Create `backend/app/services/geofence.py`:
```python
from shapely.geometry import Point, Polygon


def point_in_polygon(lat: float, lng: float, polygon_coords: list[list[float]]) -> bool:
    """Check if a point (lat, lng) is inside a polygon.

    polygon_coords: list of [lng, lat] pairs (GeoJSON convention).
    """
    poly = Polygon(polygon_coords)
    point = Point(lng, lat)
    return poly.contains(point) or poly.boundary.contains(point)


def find_zone(
    lat: float, lng: float, zones: list[dict]
) -> str | None:
    """Find which zone a point is in. Returns zone id or None."""
    for zone in zones:
        if point_in_polygon(lat, lng, zone["polygon"]):
            return zone["id"]
    return None
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/test_geofence.py -v
```

Expected: 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: geofence service with point-in-polygon"
```

---

## Task 6: WebSocket Manager

**Files:**
- Create: `backend/app/services/ws_manager.py`
- Modify: `backend/app/api/ws.py`

- [ ] **Step 1: Write WebSocket manager**

Create `backend/app/services/ws_manager.py`:
```python
import json

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._connections: dict[str, list[WebSocket]] = {}  # event_id -> connections

    async def connect(self, event_id: str, websocket: WebSocket):
        await websocket.accept()
        if event_id not in self._connections:
            self._connections[event_id] = []
        self._connections[event_id].append(websocket)

    def disconnect(self, event_id: str, websocket: WebSocket):
        if event_id in self._connections:
            self._connections[event_id].remove(websocket)

    async def broadcast(self, event_id: str, message: dict):
        if event_id not in self._connections:
            return
        dead = []
        for ws in self._connections[event_id]:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._connections[event_id].remove(ws)


ws_manager = ConnectionManager()
```

- [ ] **Step 2: Write WebSocket endpoint**

Create `backend/app/api/__init__.py`:
```python
```

Create `backend/app/api/ws.py`:
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.ws_manager import ws_manager

router = APIRouter()


@router.websocket("/ws/events/{event_id}")
async def event_websocket(websocket: WebSocket, event_id: str):
    await ws_manager.connect(event_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive, ignore incoming
    except WebSocketDisconnect:
        ws_manager.disconnect(event_id, websocket)
```

- [ ] **Step 3: Register router in main.py**

Update `backend/app/main.py` — add after CORS middleware:
```python
from app.api.ws import router as ws_router

app.include_router(ws_router)
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: WebSocket manager and endpoint"
```

---

## Task 7: REST API Endpoints

**Files:**
- Create: `backend/app/api/events.py`
- Create: `backend/app/api/staff.py`
- Create: `backend/app/api/visitors.py`
- Create: `backend/app/api/emergency.py`
- Create: `backend/app/api/simulation.py`
- Modify: `backend/app/main.py`

- [ ] **Step 1: Write events API**

Create `backend/app/api/events.py`:
```python
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventListResponse, EventResponse

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=list[EventListResponse])
async def list_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event))
    return result.scalars().all()


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Event).where(Event.id == event_id).options(selectinload(Event.zones))
    )
    return result.scalar_one()
```

- [ ] **Step 2: Write staff API**

Create `backend/app/api/staff.py`:
```python
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.staff import Staff
from app.schemas.staff import StaffResponse

router = APIRouter(prefix="/api/events", tags=["staff"])


@router.get("/{event_id}/staff", response_model=list[StaffResponse])
async def list_staff(event_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Staff).where(Staff.event_id == event_id))
    return result.scalars().all()
```

- [ ] **Step 3: Write visitors API**

Create `backend/app/api/visitors.py`:
```python
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.visitor import Visitor
from app.schemas.visitor import VisitorResponse

router = APIRouter(prefix="/api/events", tags=["visitors"])


@router.get("/{event_id}/visitors", response_model=list[VisitorResponse])
async def list_visitors(event_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Visitor).where(Visitor.event_id == event_id))
    return result.scalars().all()
```

- [ ] **Step 4: Write emergency API (SOS)**

Create `backend/app/api/emergency.py`:
```python
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
```

- [ ] **Step 5: Write simulation API (stub — engine comes in Task 9)**

Create `backend/app/api/simulation.py`:
```python
from uuid import UUID

from fastapi import APIRouter

router = APIRouter(prefix="/api/simulation", tags=["simulation"])


# Simulation state tracked in memory
_running: dict[str, bool] = {}


@router.post("/start/{event_id}")
async def start_simulation(event_id: UUID):
    from app.services.simulation import start_simulation

    await start_simulation(str(event_id))
    return {"status": "started", "event_id": str(event_id)}


@router.post("/stop/{event_id}")
async def stop_simulation(event_id: UUID):
    from app.services.simulation import stop_simulation

    await stop_simulation(str(event_id))
    return {"status": "stopped", "event_id": str(event_id)}
```

- [ ] **Step 6: Register all routers in main.py**

Replace `backend/app/main.py`:
```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.emergency import router as emergency_router
from app.api.events import router as events_router
from app.api.simulation import router as simulation_router
from app.api.staff import router as staff_router
from app.api.visitors import router as visitors_router
from app.api.ws import router as ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: run seed if DB is empty
    from app.seed import seed_if_empty

    await seed_if_empty()
    yield


app = FastAPI(title="StageFlow API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router)
app.include_router(staff_router)
app.include_router(visitors_router)
app.include_router(simulation_router)
app.include_router(emergency_router)
app.include_router(ws_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: REST API endpoints for events, staff, visitors, emergency, simulation"
```

---

## Task 8: Emergency Service

**Files:**
- Create: `backend/app/services/emergency.py`
- Create: `backend/app/services/qod.py`
- Create: `backend/tests/test_emergency.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_emergency.py`:
```python
import math

from app.services.emergency import find_nearest_medic


def test_find_nearest_medic():
    staff = [
        {"id": "s1", "role": "security", "current_lat": 41.0, "current_lng": 2.0},
        {"id": "s2", "role": "medical", "current_lat": 41.001, "current_lng": 2.001},
        {"id": "s3", "role": "medical", "current_lat": 41.01, "current_lng": 2.01},
    ]
    medic = find_nearest_medic(staff, lat=41.0, lng=2.0)
    assert medic is not None
    assert medic["id"] == "s2"


def test_find_nearest_medic_no_medics():
    staff = [
        {"id": "s1", "role": "security", "current_lat": 41.0, "current_lng": 2.0},
    ]
    medic = find_nearest_medic(staff, lat=41.0, lng=2.0)
    assert medic is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_emergency.py -v
```

Expected: FAIL

- [ ] **Step 3: Write QoD orchestration service**

Create `backend/app/services/qod.py`:
```python
from app.config import settings
from app.nokia.base import NokiaClient
from app.nokia.mock import MockNokiaClient
from app.nokia.real import RealNokiaClient

_client: NokiaClient | None = None


def get_nokia_client() -> NokiaClient:
    global _client
    if _client is None:
        if settings.nokia_mode == "real":
            _client = RealNokiaClient(settings.nokia_api_key, settings.nokia_api_secret)
        else:
            _client = MockNokiaClient()
    return _client


async def activate_qod(device_id: str, role: str) -> str:
    """Activate QoD for a device based on role.

    Staff (security, medical, logistics, operations, comms) -> QOS_L, no duration limit
    VIP -> QOS_M, 900 seconds (15 minutes)
    """
    client = get_nokia_client()
    if role == "vip":
        return await client.create_qod_session(device_id, "QOS_M", duration=900)
    else:
        return await client.create_qod_session(device_id, "QOS_L", duration=None)


async def deactivate_qod(session_id: str) -> bool:
    client = get_nokia_client()
    return await client.delete_qod_session(session_id)
```

- [ ] **Step 4: Write emergency service**

Create `backend/app/services/emergency.py`:
```python
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
    """Approximate distance in meters using Haversine."""
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
    # Find nearest medic
    result = await db.execute(select(Staff).where(Staff.role == "medical"))
    medics_models = result.scalars().all()
    staff_dicts = [
        {"id": str(m.id), "role": m.role, "current_lat": m.current_lat, "current_lng": m.current_lng}
        for m in medics_models
    ]
    medic_dict = find_nearest_medic(staff_dicts, request.lat, request.lng)

    incident = Incident(
        event_id=None,  # will be set from visitor
        type="medical_emergency",
        status="responding" if medic_dict else "open",
        reporter_id=request.visitor_id,
        responder_id=UUID(medic_dict["id"]) if medic_dict else None,
        lat=request.lat,
        lng=request.lng,
    )

    # Get visitor to find event_id
    from app.models.visitor import Visitor

    visitor_result = await db.execute(select(Visitor).where(Visitor.id == request.visitor_id))
    visitor = visitor_result.scalar_one()
    incident.event_id = visitor.event_id

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

    # Broadcast to WebSocket
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
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python -m pytest tests/test_emergency.py -v
```

Expected: 2 tests PASS

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: emergency SOS service with nearest medic lookup and QoD boost"
```

---

## Task 9: Simulation Engine

**Files:**
- Create: `backend/app/services/simulation.py`
- Create: `backend/tests/test_simulation.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_simulation.py`:
```python
from app.services.simulation import interpolate_position


def test_interpolate_position_at_start():
    waypoints = [
        {"lat": 41.0, "lng": 2.0, "offset": 0},
        {"lat": 41.1, "lng": 2.1, "offset": 10},
    ]
    lat, lng = interpolate_position(waypoints, elapsed=0)
    assert lat == 41.0
    assert lng == 2.0


def test_interpolate_position_midway():
    waypoints = [
        {"lat": 41.0, "lng": 2.0, "offset": 0},
        {"lat": 42.0, "lng": 3.0, "offset": 10},
    ]
    lat, lng = interpolate_position(waypoints, elapsed=5)
    assert abs(lat - 41.5) < 0.01
    assert abs(lng - 2.5) < 0.01


def test_interpolate_position_past_end():
    waypoints = [
        {"lat": 41.0, "lng": 2.0, "offset": 0},
        {"lat": 42.0, "lng": 3.0, "offset": 10},
    ]
    lat, lng = interpolate_position(waypoints, elapsed=20)
    assert lat == 42.0
    assert lng == 3.0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_simulation.py -v
```

Expected: FAIL

- [ ] **Step 3: Write simulation engine**

Create `backend/app/services/simulation.py`:
```python
import asyncio
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.event import Zone
from app.models.simulation_path import SimulationPath
from app.models.staff import Staff
from app.models.visitor import Visitor
from app.services.geofence import find_zone
from app.services.qod import activate_qod, deactivate_qod
from app.services.ws_manager import ws_manager

_tasks: dict[str, asyncio.Task] = {}
_running: dict[str, bool] = {}

# Crowd level script: {offset_seconds: {zone_name: level}}
CROWD_SCRIPT = {
    30: {"Main Stage A": "high"},
    45: {"Main Stage A": "critical"},
    60: {"Medium Stage 1": "high"},
}


def interpolate_position(
    waypoints: list[dict], elapsed: float
) -> tuple[float, float]:
    """Given waypoints with offset (seconds), interpolate position at elapsed time."""
    if not waypoints:
        return (0.0, 0.0)

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
    """One simulation tick: move entities, check zones, update QoD, broadcast."""

    # Load zones
    zone_result = await db.execute(select(Zone).where(Zone.event_id == event_id))
    zones = zone_result.scalars().all()
    zone_dicts = [{"id": str(z.id), "name": z.name, "polygon": z.polygon} for z in zones]
    zone_map = {str(z.id): z for z in zones}
    zone_name_map = {z.name: z for z in zones}

    # Load paths
    path_result = await db.execute(select(SimulationPath).where(SimulationPath.event_id == event_id))
    paths = path_result.scalars().all()

    for path in paths:
        lat, lng = interpolate_position(path.waypoints, elapsed)

        # Get entity
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

        # Broadcast position
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
    """Main simulation loop."""
    start_time = asyncio.get_event_loop().time()
    _running[event_id] = True

    while _running.get(event_id, False):
        elapsed = asyncio.get_event_loop().time() - start_time
        async with async_session() as db:
            await _tick(event_id, elapsed, db)
        await asyncio.sleep(2)


async def start_simulation(event_id: str):
    if event_id in _tasks and not _tasks[event_id].done():
        return  # Already running
    _tasks[event_id] = asyncio.create_task(_run_simulation(event_id))


async def stop_simulation(event_id: str):
    _running[event_id] = False
    if event_id in _tasks:
        _tasks[event_id].cancel()
        del _tasks[event_id]
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/test_simulation.py -v
```

Expected: 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: simulation engine with movement, geofence triggers, QoD, crowd levels"
```

---

## Task 10: Seed Data

**Files:**
- Create: `backend/app/seed.py`

- [ ] **Step 1: Write seed script**

Create `backend/app/seed.py`:
```python
"""Seed database with two demo events, zones, staff, visitors, and simulation paths."""

from sqlalchemy import select
from app.database import async_session
from app.models.event import Event, Zone
from app.models.staff import Staff
from app.models.visitor import Visitor
from app.models.simulation_path import SimulationPath


# ============================================================
# Event 1: Primeweaver Sound 2026, Barcelona (Fira Barcelona)
# Center: 41.3544, 2.1283
# ============================================================

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

# Waypoints: lat/lng with offset in seconds from simulation start
PRIMEWEAVER_STAFF_PATHS = {
    "Juan Garcia": [
        {"lat": 41.3495, "lng": 2.1240, "offset": 0},    # outside, south
        {"lat": 41.3510, "lng": 2.1242, "offset": 10},    # moving north
        {"lat": 41.3558, "lng": 2.1250, "offset": 20},    # enters Main Stage A
        {"lat": 41.3560, "lng": 2.1255, "offset": 40},    # inside Main Stage A
        {"lat": 41.3558, "lng": 2.1250, "offset": 50},    # still inside
        {"lat": 41.3548, "lng": 2.1250, "offset": 60},    # exits south
        {"lat": 41.3530, "lng": 2.1250, "offset": 70},    # outside
    ],
    "Dr. Maria Lopez": [
        {"lat": 41.3510, "lng": 2.1265, "offset": 0},     # at Medical Tent
        {"lat": 41.3510, "lng": 2.1265, "offset": 120},    # stays there
    ],
    "Carlos Ruiz": [
        {"lat": 41.3540, "lng": 2.1245, "offset": 0},     # near Medium Stage 1
        {"lat": 41.3540, "lng": 2.1264, "offset": 15},     # to Medium Stage 2
        {"lat": 41.3540, "lng": 2.1282, "offset": 30},     # to Medium Stage 3
        {"lat": 41.3540, "lng": 2.1264, "offset": 45},     # back to Medium Stage 2
        {"lat": 41.3540, "lng": 2.1245, "offset": 60},     # back to Medium Stage 1
    ],
    "Elena Torres": [
        {"lat": 41.3505, "lng": 2.1237, "offset": 0},     # at Entrance Gate
        {"lat": 41.3505, "lng": 2.1237, "offset": 120},    # stays there
    ],
    "Pedro Sanchez": [
        {"lat": 41.3560, "lng": 2.1245, "offset": 0},     # near Main Stage A
        {"lat": 41.3560, "lng": 2.1280, "offset": 20},     # to Main Stage B
        {"lat": 41.3560, "lng": 2.1310, "offset": 40},     # to Food Court
        {"lat": 41.3560, "lng": 2.1280, "offset": 60},     # back
        {"lat": 41.3560, "lng": 2.1245, "offset": 80},     # back to start
    ],
}

PRIMEWEAVER_VISITOR_PATHS = {
    "Anna Berg": [
        {"lat": 41.3505, "lng": 2.1237, "offset": 0},     # at Entrance
        {"lat": 41.3530, "lng": 2.1270, "offset": 15},     # walking north
        {"lat": 41.3565, "lng": 2.1305, "offset": 25},     # enters VIP Area
        {"lat": 41.3566, "lng": 2.1308, "offset": 55},     # stays in VIP
        {"lat": 41.3560, "lng": 2.1310, "offset": 70},     # moves to Food Court
    ],
    "Visitor X": [
        {"lat": 41.3552, "lng": 2.1248, "offset": 0},     # near Main Stage A (outside, watching)
        {"lat": 41.3552, "lng": 2.1248, "offset": 120},    # stationary — will press SOS manually
    ],
}


# ============================================================
# Event 2: World Cup 2026, Mexico City (Estadio Azteca)
# Center: 19.3029, -99.1505
# ============================================================

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
    """Seed the database if no events exist."""
    from app.database import engine, Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        result = await db.execute(select(Event))
        if result.scalars().first() is not None:
            return  # Already seeded

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

    # Zones
    zone_objects = []
    for z in zones:
        zone = Zone(event_id=event.id, name=z["name"], type=z.get("type", "general"), polygon=z["polygon"], color=z.get("color", "#3B82F6"))
        db.add(zone)
        zone_objects.append(zone)
    await db.flush()

    # Staff
    staff_map = {}
    for s in staff:
        obj = Staff(event_id=event.id, name=s["name"], phone=s["phone"], role=s["role"], device_id=s["device_id"])
        db.add(obj)
        staff_map[s["name"]] = obj
    await db.flush()

    # Visitors
    visitor_map = {}
    for v in visitors:
        obj = Visitor(event_id=event.id, name=v["name"], phone=v["phone"], type=v["type"], device_id=v["device_id"])
        db.add(obj)
        visitor_map[v["name"]] = obj
    await db.flush()

    # Staff paths
    for name, waypoints in staff_paths.items():
        if name in staff_map:
            path = SimulationPath(event_id=event.id, entity_type="staff", entity_id=staff_map[name].id, waypoints=waypoints)
            db.add(path)

    # Visitor paths
    for name, waypoints in visitor_paths.items():
        if name in visitor_map:
            path = SimulationPath(event_id=event.id, entity_type="visitor", entity_id=visitor_map[name].id, waypoints=waypoints)
            db.add(path)
```

- [ ] **Step 2: Verify seed runs**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026
docker-compose up -d postgres
cd backend
DATABASE_URL=postgresql+asyncpg://stageflow:stageflow@localhost:5432/stageflow python -c "
import asyncio
from app.seed import seed_if_empty
asyncio.run(seed_if_empty())
print('Seed complete')
"
```

Expected: "Seed complete", no errors.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat: seed data for Primeweaver Sound and World Cup events"
```

---

## Task 11: Frontend — API Client & WebSocket Hook

**Files:**
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/hooks/useWebSocket.ts`
- Create: `frontend/src/hooks/useEvents.ts`

- [ ] **Step 1: Write API client**

Create `frontend/src/api/client.ts`:
```typescript
const API_BASE = "/api";

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  getEvents: () => fetchJson<import("../types").EventListItem[]>("/events"),
  getEvent: (id: string) => fetchJson<import("../types").Event>(`/events/${id}`),
  getStaff: (eventId: string) => fetchJson<import("../types").Staff[]>(`/events/${eventId}/staff`),
  getVisitors: (eventId: string) => fetchJson<import("../types").Visitor[]>(`/events/${eventId}/visitors`),
  startSimulation: (eventId: string) => fetchJson(`/simulation/start/${eventId}`, { method: "POST" }),
  stopSimulation: (eventId: string) => fetchJson(`/simulation/stop/${eventId}`, { method: "POST" }),
  triggerSos: (visitorId: string, lat: number, lng: number) =>
    fetchJson<import("../types").Incident>("/emergency/sos", {
      method: "POST",
      body: JSON.stringify({ visitor_id: visitorId, lat, lng }),
    }),
  resolveIncident: (incidentId: string) =>
    fetchJson<import("../types").Incident>(`/emergency/${incidentId}/resolve`, { method: "POST" }),
};
```

- [ ] **Step 2: Write WebSocket hook**

Create `frontend/src/hooks/useWebSocket.ts`:
```typescript
import { useEffect, useRef, useCallback, useState } from "react";
import type { WsMessage, LogEntry } from "../types";

interface UseWebSocketReturn {
  messages: WsMessage[];
  logs: LogEntry[];
  connected: boolean;
}

export function useWebSocket(eventId: string | null): UseWebSocketReturn {
  const wsRef = useRef<WebSocket | null>(null);
  const [messages, setMessages] = useState<WsMessage[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!eventId) return;

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/events/${eventId}`);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);

    ws.onmessage = (event) => {
      const msg: WsMessage = JSON.parse(event.data);
      setMessages((prev) => [...prev.slice(-200), msg]); // Keep last 200

      if (msg.type === "log") {
        const entry: LogEntry = {
          id: crypto.randomUUID(),
          timestamp: new Date().toISOString(),
          message: (msg.data as Record<string, string>).message,
          level: (msg.data as Record<string, string>).level as LogEntry["level"],
        };
        setLogs((prev) => [...prev.slice(-100), entry]);
      }
    };

    return () => {
      ws.close();
      setConnected(false);
    };
  }, [eventId]);

  return { messages, logs, connected };
}
```

- [ ] **Step 3: Write useEvents hook**

Create `frontend/src/hooks/useEvents.ts`:
```typescript
import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { EventListItem } from "../types";

export function useEvents() {
  const [events, setEvents] = useState<EventListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getEvents().then((data) => {
      setEvents(data);
      setLoading(false);
    });
  }, []);

  return { events, loading };
}
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: frontend API client and WebSocket hook"
```

---

## Task 12: Frontend — Dashboard with Map

**Files:**
- Create: `frontend/src/pages/Dashboard/DashboardPage.tsx`
- Create: `frontend/src/pages/Dashboard/EventMap.tsx`
- Create: `frontend/src/pages/Dashboard/ZonePolygon.tsx`
- Create: `frontend/src/pages/Dashboard/EntityMarker.tsx`
- Create: `frontend/src/pages/Dashboard/IncidentMarker.tsx`
- Create: `frontend/src/pages/Dashboard/StaffPanel.tsx`
- Create: `frontend/src/pages/Dashboard/EventLog.tsx`
- Create: `frontend/src/pages/Dashboard/EventSelector.tsx`
- Create: `frontend/src/pages/Dashboard/SimControls.tsx`
- Modify: `frontend/src/App.tsx`

This is the largest task — the main dashboard view. Each step creates one component.

- [ ] **Step 1: Create EventSelector**

Create `frontend/src/pages/Dashboard/EventSelector.tsx`:
```tsx
import type { EventListItem } from "../../types";

interface Props {
  events: EventListItem[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export function EventSelector({ events, selectedId, onSelect }: Props) {
  return (
    <select
      className="bg-gray-800 text-white border border-gray-600 rounded px-3 py-2 text-sm"
      value={selectedId ?? ""}
      onChange={(e) => onSelect(e.target.value)}
    >
      <option value="" disabled>Select event...</option>
      {events.map((ev) => (
        <option key={ev.id} value={ev.id}>
          {ev.name} — {ev.city}, {ev.country}
        </option>
      ))}
    </select>
  );
}
```

- [ ] **Step 2: Create SimControls**

Create `frontend/src/pages/Dashboard/SimControls.tsx`:
```tsx
import { api } from "../../api/client";
import { useState } from "react";

interface Props {
  eventId: string;
}

export function SimControls({ eventId }: Props) {
  const [running, setRunning] = useState(false);

  const handleStart = async () => {
    await api.startSimulation(eventId);
    setRunning(true);
  };

  const handleStop = async () => {
    await api.stopSimulation(eventId);
    setRunning(false);
  };

  return (
    <div className="flex gap-2">
      {!running ? (
        <button
          onClick={handleStart}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm font-medium"
        >
          Start Simulation
        </button>
      ) : (
        <button
          onClick={handleStop}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm font-medium"
        >
          Stop Simulation
        </button>
      )}
    </div>
  );
}
```

- [ ] **Step 3: Create ZonePolygon**

Create `frontend/src/pages/Dashboard/ZonePolygon.tsx`:
```tsx
import { Polygon, Tooltip } from "react-leaflet";
import type { Zone } from "../../types";

const CROWD_COLORS: Record<string, string> = {
  low: "#22C55E",
  medium: "#EAB308",
  high: "#F97316",
  critical: "#EF4444",
};

interface Props {
  zone: Zone;
}

export function ZonePolygon({ zone }: Props) {
  // GeoJSON is [lng, lat], Leaflet wants [lat, lng]
  const positions = zone.polygon.map(([lng, lat]) => [lat, lng] as [number, number]);
  const fillColor = zone.crowd_level !== "low" ? CROWD_COLORS[zone.crowd_level] : zone.color;

  return (
    <Polygon
      positions={positions}
      pathOptions={{
        color: zone.color,
        fillColor,
        fillOpacity: zone.crowd_level === "critical" ? 0.5 : 0.25,
        weight: 2,
      }}
    >
      <Tooltip sticky>
        <strong>{zone.name}</strong>
        <br />
        Crowd: {zone.crowd_level.toUpperCase()}
      </Tooltip>
    </Polygon>
  );
}
```

- [ ] **Step 4: Create EntityMarker**

Create `frontend/src/pages/Dashboard/EntityMarker.tsx`:
```tsx
import { CircleMarker, Tooltip } from "react-leaflet";

interface Props {
  name: string;
  role: string;
  lat: number;
  lng: number;
  qodActive: boolean;
  entityType: "staff" | "visitor";
}

const ROLE_COLORS: Record<string, string> = {
  security: "#3B82F6",
  medical: "#EF4444",
  logistics: "#F59E0B",
  operations: "#8B5CF6",
  comms: "#06B6D4",
  vip: "#EC4899",
  regular: "#9CA3AF",
};

export function EntityMarker({ name, role, lat, lng, qodActive, entityType }: Props) {
  const color = ROLE_COLORS[role] ?? "#6B7280";

  return (
    <CircleMarker
      center={[lat, lng]}
      radius={qodActive ? 10 : 7}
      pathOptions={{
        color: qodActive ? "#22C55E" : color,
        fillColor: color,
        fillOpacity: 0.8,
        weight: qodActive ? 3 : 1,
      }}
    >
      <Tooltip>
        <strong>{name}</strong>
        <br />
        {entityType === "staff" ? `Role: ${role}` : `Type: ${role}`}
        <br />
        QoD: {qodActive ? "ACTIVE" : "inactive"}
      </Tooltip>
    </CircleMarker>
  );
}
```

- [ ] **Step 5: Create IncidentMarker**

Create `frontend/src/pages/Dashboard/IncidentMarker.tsx`:
```tsx
import { CircleMarker, Polyline, Tooltip } from "react-leaflet";

interface Props {
  lat: number;
  lng: number;
  responderLat?: number;
  responderLng?: number;
  status: string;
}

export function IncidentMarker({ lat, lng, responderLat, responderLng, status }: Props) {
  if (status === "resolved") return null;

  return (
    <>
      <CircleMarker
        center={[lat, lng]}
        radius={14}
        pathOptions={{ color: "#EF4444", fillColor: "#EF4444", fillOpacity: 0.6, weight: 3 }}
      >
        <Tooltip>SOS — {status}</Tooltip>
      </CircleMarker>
      {responderLat && responderLng && (
        <Polyline
          positions={[[lat, lng], [responderLat, responderLng]]}
          pathOptions={{ color: "#EF4444", dashArray: "8 4", weight: 2 }}
        />
      )}
    </>
  );
}
```

- [ ] **Step 6: Create StaffPanel**

Create `frontend/src/pages/Dashboard/StaffPanel.tsx`:
```tsx
import type { Staff, Visitor } from "../../types";
import { QodBadge } from "../../components/QodBadge";

interface Props {
  staff: Staff[];
  visitors: Visitor[];
}

export function StaffPanel({ staff, visitors }: Props) {
  return (
    <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto max-h-[400px]">
      <h3 className="text-white font-semibold mb-3">Staff</h3>
      {staff.map((s) => (
        <div key={s.id} className="flex items-center justify-between py-2 border-b border-gray-700">
          <div>
            <span className="text-white text-sm">{s.name}</span>
            <span className="text-gray-400 text-xs ml-2">{s.role}</span>
          </div>
          <QodBadge active={s.qod_status === "active"} />
        </div>
      ))}
      <h3 className="text-white font-semibold mb-3 mt-4">Visitors</h3>
      {visitors.map((v) => (
        <div key={v.id} className="flex items-center justify-between py-2 border-b border-gray-700">
          <div>
            <span className="text-white text-sm">{v.name}</span>
            <span className="text-gray-400 text-xs ml-2">{v.type}</span>
          </div>
          <QodBadge active={v.qod_status === "active"} />
        </div>
      ))}
    </div>
  );
}
```

- [ ] **Step 7: Create QodBadge component**

Create `frontend/src/components/QodBadge.tsx`:
```tsx
interface Props {
  active: boolean;
}

export function QodBadge({ active }: Props) {
  return (
    <span
      className={`text-xs px-2 py-1 rounded-full font-medium ${
        active ? "bg-green-600 text-white" : "bg-gray-600 text-gray-300"
      }`}
    >
      {active ? "Priority Active" : "Normal"}
    </span>
  );
}
```

- [ ] **Step 8: Create EventLog**

Create `frontend/src/pages/Dashboard/EventLog.tsx`:
```tsx
import type { LogEntry } from "../../types";

interface Props {
  logs: LogEntry[];
}

const LEVEL_STYLES: Record<string, string> = {
  info: "text-blue-400",
  success: "text-green-400",
  warning: "text-yellow-400",
  critical: "text-red-400",
};

export function EventLog({ logs }: Props) {
  return (
    <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto max-h-[300px]">
      <h3 className="text-white font-semibold mb-3">Event Log</h3>
      <div className="space-y-1">
        {[...logs].reverse().map((log) => (
          <div key={log.id} className="text-xs font-mono">
            <span className="text-gray-500">{new Date(log.timestamp).toLocaleTimeString()}</span>{" "}
            <span className={LEVEL_STYLES[log.level] ?? "text-gray-300"}>{log.message}</span>
          </div>
        ))}
        {logs.length === 0 && <div className="text-gray-500 text-xs">No events yet. Start simulation.</div>}
      </div>
    </div>
  );
}
```

- [ ] **Step 9: Create EventMap**

Create `frontend/src/pages/Dashboard/EventMap.tsx`:
```tsx
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { Event, Staff, Visitor, Incident } from "../../types";
import { ZonePolygon } from "./ZonePolygon";
import { EntityMarker } from "./EntityMarker";
import { IncidentMarker } from "./IncidentMarker";

interface Props {
  event: Event;
  staff: Staff[];
  visitors: Visitor[];
  incidents: Incident[];
}

export function EventMap({ event, staff, visitors, incidents }: Props) {
  const center: [number, number] = [
    (event.bounds.north + event.bounds.south) / 2,
    (event.bounds.east + event.bounds.west) / 2,
  ];

  return (
    <MapContainer center={center} zoom={16} className="h-full w-full rounded-lg" scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {event.zones.map((zone) => (
        <ZonePolygon key={zone.id} zone={zone} />
      ))}
      {staff
        .filter((s) => s.current_lat && s.current_lng)
        .map((s) => (
          <EntityMarker
            key={s.id}
            name={s.name}
            role={s.role}
            lat={s.current_lat!}
            lng={s.current_lng!}
            qodActive={s.qod_status === "active"}
            entityType="staff"
          />
        ))}
      {visitors
        .filter((v) => v.current_lat && v.current_lng)
        .map((v) => (
          <EntityMarker
            key={v.id}
            name={v.name}
            role={v.type}
            lat={v.current_lat!}
            lng={v.current_lng!}
            qodActive={v.qod_status === "active"}
            entityType="visitor"
          />
        ))}
      {incidents.map((inc) => {
        const responder = staff.find((s) => s.id === inc.responder_id);
        return (
          <IncidentMarker
            key={inc.id}
            lat={inc.lat}
            lng={inc.lng}
            responderLat={responder?.current_lat ?? undefined}
            responderLng={responder?.current_lng ?? undefined}
            status={inc.status}
          />
        );
      })}
    </MapContainer>
  );
}
```

- [ ] **Step 10: Create DashboardPage**

Create `frontend/src/pages/Dashboard/DashboardPage.tsx`:
```tsx
import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { useEvents } from "../../hooks/useEvents";
import { useWebSocket } from "../../hooks/useWebSocket";
import type { Event, Staff, Visitor, Incident, WsMessage } from "../../types";
import { EventSelector } from "./EventSelector";
import { SimControls } from "./SimControls";
import { EventMap } from "./EventMap";
import { StaffPanel } from "./StaffPanel";
import { EventLog } from "./EventLog";

export function DashboardPage() {
  const { events, loading } = useEvents();
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);
  const [event, setEvent] = useState<Event | null>(null);
  const [staff, setStaff] = useState<Staff[]>([]);
  const [visitors, setVisitors] = useState<Visitor[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const { messages, logs, connected } = useWebSocket(selectedEventId);

  // Auto-select first event
  useEffect(() => {
    if (events.length > 0 && !selectedEventId) {
      setSelectedEventId(events[0].id);
    }
  }, [events, selectedEventId]);

  // Load event data when selection changes
  useEffect(() => {
    if (!selectedEventId) return;
    Promise.all([
      api.getEvent(selectedEventId),
      api.getStaff(selectedEventId),
      api.getVisitors(selectedEventId),
    ]).then(([ev, st, vis]) => {
      setEvent(ev);
      setStaff(st);
      setVisitors(vis);
      setIncidents([]);
    });
  }, [selectedEventId]);

  // Process WebSocket messages
  useEffect(() => {
    if (messages.length === 0) return;
    const msg = messages[messages.length - 1];

    if (msg.type === "position_update") {
      const d = msg.data as { entity_id: string; entity_type: string; lat: number; lng: number; zone_id: string | null };
      if (d.entity_type === "staff") {
        setStaff((prev) => prev.map((s) => (s.id === d.entity_id ? { ...s, current_lat: d.lat, current_lng: d.lng, current_zone_id: d.zone_id } : s)));
      } else {
        setVisitors((prev) => prev.map((v) => (v.id === d.entity_id ? { ...v, current_lat: d.lat, current_lng: d.lng, current_zone_id: d.zone_id } : v)));
      }
    }

    if (msg.type === "qod_update") {
      const d = msg.data as { entity_id: string; entity_type: string; qod_status: string; session_id?: string };
      if (d.entity_type === "staff") {
        setStaff((prev) => prev.map((s) => (s.id === d.entity_id ? { ...s, qod_status: d.qod_status as "active" | "inactive", qod_session_id: d.session_id ?? null } : s)));
      } else {
        setVisitors((prev) => prev.map((v) => (v.id === d.entity_id ? { ...v, qod_status: d.qod_status as "active" | "inactive", qod_session_id: d.session_id ?? null } : v)));
      }
    }

    if (msg.type === "zone_update" && event) {
      const d = msg.data as { zone_id: string; crowd_level: string };
      setEvent((prev) => prev ? {
        ...prev,
        zones: prev.zones.map((z) => (z.id === d.zone_id ? { ...z, crowd_level: d.crowd_level as any } : z)),
      } : prev);
    }

    if (msg.type === "incident") {
      const d = msg.data as Incident;
      setIncidents((prev) => {
        const existing = prev.findIndex((i) => i.id === d.id);
        if (existing >= 0) {
          const updated = [...prev];
          updated[existing] = { ...updated[existing], ...d };
          return updated;
        }
        return [...prev, d as Incident];
      });
    }
  }, [messages]);

  if (loading) return <div className="bg-gray-900 min-h-screen text-white p-8">Loading...</div>;

  return (
    <div className="bg-gray-900 min-h-screen text-white">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700">
        <h1 className="text-xl font-bold">StageFlow</h1>
        <div className="flex items-center gap-4">
          <EventSelector events={events} selectedId={selectedEventId} onSelect={setSelectedEventId} />
          {selectedEventId && <SimControls eventId={selectedEventId} />}
          <span className={`text-xs ${connected ? "text-green-400" : "text-red-400"}`}>
            {connected ? "Live" : "Disconnected"}
          </span>
        </div>
      </div>

      {/* Main content */}
      <div className="flex h-[calc(100vh-73px)]">
        {/* Map */}
        <div className="flex-1 p-4">
          {event && <EventMap event={event} staff={staff} visitors={visitors} incidents={incidents} />}
        </div>

        {/* Side panel */}
        <div className="w-80 p-4 space-y-4 overflow-y-auto border-l border-gray-700">
          <StaffPanel staff={staff} visitors={visitors} />
          <EventLog logs={logs} />
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 11: Update App.tsx to use DashboardPage**

Replace `frontend/src/App.tsx`:
```tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { DashboardPage } from "./pages/Dashboard/DashboardPage";
import { StaffPage } from "./pages/Staff/StaffPage";
import { VisitorPage } from "./pages/Visitor/VisitorPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/staff" element={<StaffPage />} />
        <Route path="/visitor" element={<VisitorPage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

Create placeholder `frontend/src/pages/Staff/StaffPage.tsx`:
```tsx
export function StaffPage() {
  return <div className="p-4 min-h-screen bg-white">Staff view — coming next</div>;
}
```

Create placeholder `frontend/src/pages/Visitor/VisitorPage.tsx`:
```tsx
export function VisitorPage() {
  return <div className="p-4 min-h-screen bg-white">Visitor view — coming next</div>;
}
```

- [ ] **Step 12: Verify dashboard renders**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026
docker-compose up
```

Open `http://localhost:3000` — should see dark dashboard with event dropdown, map with zones, empty staff panel, empty event log.

- [ ] **Step 13: Commit**

```bash
git add -A
git commit -m "feat: dashboard with map, zones, staff panel, event log, simulation controls"
```

---

## Task 13: Frontend — Staff Mobile View

**Files:**
- Create: `frontend/src/pages/Staff/StaffPage.tsx` (replace placeholder)

- [ ] **Step 1: Write StaffPage**

Replace `frontend/src/pages/Staff/StaffPage.tsx`:
```tsx
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../../api/client";
import { useWebSocket } from "../../hooks/useWebSocket";
import { QodBadge } from "../../components/QodBadge";
import type { Staff } from "../../types";

export function StaffPage() {
  const [searchParams] = useSearchParams();
  const staffId = searchParams.get("id");
  const eventId = searchParams.get("event");
  const [staff, setStaff] = useState<Staff | null>(null);
  const [alert, setAlert] = useState<string | null>(null);
  const { messages } = useWebSocket(eventId);

  useEffect(() => {
    if (!eventId || !staffId) return;
    api.getStaff(eventId).then((all) => {
      const me = all.find((s) => s.id === staffId);
      if (me) setStaff(me);
    });
  }, [eventId, staffId]);

  // Process WebSocket updates for this staff member
  useEffect(() => {
    if (!messages.length || !staffId) return;
    const msg = messages[messages.length - 1];

    if (msg.type === "qod_update" && (msg.data as any).entity_id === staffId) {
      setStaff((prev) => prev ? { ...prev, qod_status: (msg.data as any).qod_status } : prev);
    }

    if (msg.type === "incident") {
      const d = msg.data as any;
      if (d.responder_id === staffId && d.status !== "resolved") {
        setAlert(`Emergency! Patient ${d.distance_meters ?? "?"}m from you`);
      }
      if (d.status === "resolved") {
        setAlert(null);
      }
    }
  }, [messages, staffId]);

  if (!staff) {
    return (
      <div className="p-6 min-h-screen bg-gray-50">
        <h1 className="text-xl font-bold mb-4">StageFlow — Staff</h1>
        <p className="text-gray-500">Add ?event=EVENT_ID&id=STAFF_ID to URL</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-4 py-3">
        <h1 className="text-lg font-bold">StageFlow</h1>
      </div>

      {/* Alert */}
      {alert && (
        <div className="bg-red-600 text-white p-4 text-center font-bold animate-pulse">
          {alert}
        </div>
      )}

      {/* Status card */}
      <div className="p-4 space-y-4">
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-xl font-semibold">{staff.name}</h2>
          <p className="text-gray-500 capitalize">{staff.role}</p>
        </div>

        <div className="bg-white rounded-xl shadow p-6 text-center">
          <p className="text-sm text-gray-500 mb-2">Network Status</p>
          <div className="text-2xl font-bold mb-2">
            {staff.qod_status === "active" ? (
              <span className="text-green-600">Priority Active</span>
            ) : (
              <span className="text-gray-400">Normal</span>
            )}
          </div>
          <QodBadge active={staff.qod_status === "active"} />
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <p className="text-sm text-gray-500">Phone</p>
          <p className="font-medium">{staff.phone}</p>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Verify staff view**

Open `http://localhost:3000/staff?event=EVENT_ID&id=STAFF_ID` (use actual IDs from the seeded data).

Expected: Shows staff name, role, network status.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat: staff mobile view with QoD status and emergency alerts"
```

---

## Task 14: Frontend — Visitor Mobile View with SOS

**Files:**
- Create: `frontend/src/pages/Visitor/VisitorPage.tsx` (replace placeholder)
- Create: `frontend/src/components/SosButton.tsx`

- [ ] **Step 1: Write SosButton component**

Create `frontend/src/components/SosButton.tsx`:
```tsx
interface Props {
  onPress: () => void;
  disabled?: boolean;
}

export function SosButton({ onPress, disabled }: Props) {
  return (
    <button
      onClick={onPress}
      disabled={disabled}
      className="w-full py-6 rounded-2xl text-white text-2xl font-bold
                 bg-red-600 hover:bg-red-700 active:bg-red-800
                 disabled:bg-gray-400 disabled:cursor-not-allowed
                 shadow-lg transition-all"
    >
      {disabled ? "SOS Sent" : "SOS Emergency"}
    </button>
  );
}
```

- [ ] **Step 2: Write VisitorPage**

Replace `frontend/src/pages/Visitor/VisitorPage.tsx`:
```tsx
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../../api/client";
import { useWebSocket } from "../../hooks/useWebSocket";
import { QodBadge } from "../../components/QodBadge";
import { SosButton } from "../../components/SosButton";
import type { Visitor } from "../../types";

export function VisitorPage() {
  const [searchParams] = useSearchParams();
  const visitorId = searchParams.get("id");
  const eventId = searchParams.get("event");
  const [visitor, setVisitor] = useState<Visitor | null>(null);
  const [sosSent, setSosSent] = useState(false);
  const [sosStatus, setSosStatus] = useState<string | null>(null);
  const { messages } = useWebSocket(eventId);

  useEffect(() => {
    if (!eventId || !visitorId) return;
    api.getVisitors(eventId).then((all) => {
      const me = all.find((v) => v.id === visitorId);
      if (me) setVisitor(me);
    });
  }, [eventId, visitorId]);

  useEffect(() => {
    if (!messages.length || !visitorId) return;
    const msg = messages[messages.length - 1];

    if (msg.type === "qod_update" && (msg.data as any).entity_id === visitorId) {
      setVisitor((prev) => prev ? { ...prev, qod_status: (msg.data as any).qod_status } : prev);
    }

    if (msg.type === "incident") {
      const d = msg.data as any;
      if (d.status === "responding") {
        setSosStatus("Help is on the way!");
      }
      if (d.status === "resolved") {
        setSosStatus("Incident resolved");
        setSosSent(false);
      }
    }
  }, [messages, visitorId]);

  const handleSos = async () => {
    if (!visitor || !visitor.current_lat || !visitor.current_lng) return;
    setSosSent(true);
    setSosStatus("Sending SOS...");
    await api.triggerSos(visitor.id, visitor.current_lat, visitor.current_lng);
  };

  if (!visitor) {
    return (
      <div className="p-6 min-h-screen bg-gray-50">
        <h1 className="text-xl font-bold mb-4">StageFlow</h1>
        <p className="text-gray-500">Add ?event=EVENT_ID&id=VISITOR_ID to URL</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b px-4 py-3">
        <h1 className="text-lg font-bold">StageFlow</h1>
      </div>

      <div className="p-4 space-y-4">
        <div className="bg-white rounded-xl shadow p-6 text-center">
          <p className="text-sm text-gray-500 mb-2">Welcome, {visitor.name}</p>
          {visitor.type === "vip" && (
            <>
              <p className="text-sm text-gray-500 mb-2">Network Status</p>
              <div className="text-2xl font-bold mb-2">
                {visitor.qod_status === "active" ? (
                  <span className="text-green-600">Internet Boost Active</span>
                ) : (
                  <span className="text-gray-400">Standard</span>
                )}
              </div>
              <QodBadge active={visitor.qod_status === "active"} />
            </>
          )}
        </div>

        {/* SOS Status */}
        {sosStatus && (
          <div className={`rounded-xl p-4 text-center font-semibold ${
            sosStatus.includes("way") ? "bg-blue-100 text-blue-700" :
            sosStatus.includes("resolved") ? "bg-green-100 text-green-700" :
            "bg-yellow-100 text-yellow-700"
          }`}>
            {sosStatus}
          </div>
        )}

        {/* SOS Button */}
        <SosButton onPress={handleSos} disabled={sosSent} />
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Verify visitor view**

Open `http://localhost:3000/visitor?event=EVENT_ID&id=VISITOR_ID`

Expected: Shows visitor name, VIP boost status if applicable, red SOS button.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: visitor mobile view with SOS button and QoD boost display"
```

---

## Task 15: Integration Test — Full Demo Flow

**Files:**
- Create: `backend/tests/test_api.py`

- [ ] **Step 1: Write integration test**

Create `backend/tests/test_api.py`:
```python
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


@pytest.mark.anyio
async def test_list_events():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/events")
        assert resp.status_code == 200
        events = resp.json()
        assert len(events) >= 2
        names = [e["name"] for e in events]
        assert "Primeweaver Sound 2026" in names
        assert "World Cup 2026" in names


@pytest.mark.anyio
async def test_get_event_with_zones():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        events = (await client.get("/api/events")).json()
        primeweaver = next(e for e in events if "Primeweaver" in e["name"])

        resp = await client.get(f"/api/events/{primeweaver['id']}")
        assert resp.status_code == 200
        event = resp.json()
        assert len(event["zones"]) == 12


@pytest.mark.anyio
async def test_get_staff():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        events = (await client.get("/api/events")).json()
        primeweaver = next(e for e in events if "Primeweaver" in e["name"])

        resp = await client.get(f"/api/events/{primeweaver['id']}/staff")
        assert resp.status_code == 200
        staff = resp.json()
        assert len(staff) == 5
        roles = {s["role"] for s in staff}
        assert "medical" in roles
        assert "security" in roles
```

- [ ] **Step 2: Run tests**

```bash
cd /Users/ilebedyuk/projects/hackathon_2026/backend
python -m pytest tests/ -v
```

Expected: All tests pass.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "test: API integration tests for events, staff, and health"
```

---

## Task 16: Railway Deployment Config

**Files:**
- Create: `railway.toml` (or use Railway dashboard)
- Modify: `backend/Dockerfile` (ensure production-ready)
- Modify: `frontend/Dockerfile` (ensure production-ready)

- [ ] **Step 1: Ensure backend Dockerfile runs migrations and seed on start**

Update `backend/Dockerfile` — replace CMD:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgeos-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The seed runs automatically in the FastAPI lifespan (see main.py), so no extra start script needed.

- [ ] **Step 2: Update frontend nginx.conf for Railway**

In Railway, the backend service name may differ. Use environment variable for proxy target. For now, hardcode `backend:8000` — Railway service discovery uses the service name.

The existing `frontend/nginx.conf` and `frontend/Dockerfile` are already production-ready.

- [ ] **Step 3: Document Railway deployment steps**

Create `docs/deployment.md`:
```markdown
# Railway Deployment

## Setup

1. Create a new Railway project
2. Add PostgreSQL plugin (PostGIS not available — use regular PostgreSQL, Shapely handles geo in Python)
3. Add service from repo: `backend/` directory
   - Set env: `DATABASE_URL` (from PostgreSQL plugin), `NOKIA_MODE=mock`
4. Add service from repo: `frontend/` directory
   - Set `BACKEND_URL` env var to internal backend URL if needed
5. Set up networking: frontend is public-facing, backend is internal

## Environment Variables (backend)

- `DATABASE_URL` — provided by Railway PostgreSQL
- `NOKIA_MODE` — `mock` or `real`
- `NOKIA_API_KEY` — when available
- `NOKIA_API_SECRET` — when available

## Notes

- Backend runs seed on startup automatically
- Frontend proxies /api and /ws to backend via nginx
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "docs: Railway deployment guide"
```

---

## Summary

| Task | What | Tests |
|------|------|-------|
| 1 | Project scaffold, Docker, minimal app | Manual: docker-compose up |
| 2 | Database models, Alembic migration | Manual: migration runs |
| 3 | Pydantic schemas, TypeScript types | — (contract definition) |
| 4 | Nokia client (mock + interface) | 3 unit tests |
| 5 | Geofence service | 4 unit tests |
| 6 | WebSocket manager + endpoint | Manual |
| 7 | REST API endpoints | — (tested in Task 15) |
| 8 | Emergency SOS service | 2 unit tests |
| 9 | Simulation engine | 3 unit tests |
| 10 | Seed data (2 events) | Manual: seed runs |
| 11 | Frontend API client + hooks | Manual |
| 12 | Dashboard with map | Manual |
| 13 | Staff mobile view | Manual |
| 14 | Visitor mobile view + SOS | Manual |
| 15 | Integration tests | 4 API tests |
| 16 | Railway deployment config | Manual |

**Total: 16 tasks, ~16 unit/integration tests, estimated 16 commits.**
