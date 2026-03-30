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
    type = Column(String(20), nullable=False)
    device_id = Column(String(100), default="")
    qod_status = Column(String(20), default="inactive")
    qod_session_id = Column(String(255), nullable=True)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    current_zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=True)

    event = relationship("Event", back_populates="visitors")
    current_zone = relationship("Zone", foreign_keys=[current_zone_id])
