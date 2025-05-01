"""Glucose Response class."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class GlucoseResponse(BaseModel):
    """Response model."""

    uuid: UUID
    device: str
    device_id: UUID
    device_timestamp: datetime
    recording_type: int
    glucose_value_history: int
    glucose_scan: int
