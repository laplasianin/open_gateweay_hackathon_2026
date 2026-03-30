from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.events import router as events_router
from app.api.staff import router as staff_router
from app.api.visitors import router as visitors_router
from app.api.simulation import router as simulation_router
from app.api.emergency import router as emergency_router


@asynccontextmanager
async def lifespan(app: FastAPI):
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

# WS router - import conditionally in case ws.py exists
try:
    from app.api.ws import router as ws_router
    app.include_router(ws_router)
except ImportError:
    pass


@app.get("/api/health")
async def health():
    return {"status": "ok"}
