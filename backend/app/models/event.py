import uuid

from sqlalchemy import Column, ForeignKey, String, Text
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
    bounds = Column(JSON, nullable=False)
    status = Column(String(20), default="active")

    zones = relationship("Zone", back_populates="event", cascade="all, delete-orphan")
    staff = relationship("Staff", back_populates="event", cascade="all, delete-orphan")
    visitors = relationship("Visitor", back_populates="event", cascade="all, delete-orphan")


class Zone(Base):
    __tablename__ = "zones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    polygon = Column(JSON, nullable=False)
    crowd_level = Column(String(20), default="low")
    color = Column(String(7), default="#3B82F6")

    event = relationship("Event", back_populates="zones")
