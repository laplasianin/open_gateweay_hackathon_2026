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
