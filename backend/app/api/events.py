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
