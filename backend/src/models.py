"""Pydantic models for API responses."""
from pydantic import BaseModel
from typing import Optional
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

