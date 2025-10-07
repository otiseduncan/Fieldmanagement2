from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class JobBase(BaseModel):
    ro_number: str
    vin: str = Field(min_length=11, max_length=17)
    status: str = Field(default='pending')
    client_notes: Optional[str] = None


class JobCreate(JobBase):
    client_id: int
    metadata: dict[str, Any] = Field(default_factory=dict)


class JobUpdate(BaseModel):
    status: Optional[str] = None
    technician_notes: Optional[str] = None
    client_notes: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class JobOut(JobBase):
    id: int
    technician_id: Optional[int] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, Any]

    class Config:
        orm_mode = True
