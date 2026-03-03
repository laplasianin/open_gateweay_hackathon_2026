"""Pydantic models for API responses."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str
    timestamp: datetime
    database: str


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    detail: Optional[str] = None
    timestamp: datetime


class Marker(BaseModel):
    """Marker model for map."""
    lat: float
    lng: float
    label: str
    role: str


class MarkersUpdate(BaseModel):
    """Markers update model for WebSocket."""
    markers: List[Marker]
    timestamp: datetime


class DeviceLocation(BaseModel):
    """Device location data from NAC."""
    phone_number: str
    longitude: float
    latitude: float
    radius: Optional[float] = None


class DeviceLocationsUpdate(BaseModel):
    """Device locations update model for WebSocket."""
    devices: List[DeviceLocation]
    timestamp: datetime

