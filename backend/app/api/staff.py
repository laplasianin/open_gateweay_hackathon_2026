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
