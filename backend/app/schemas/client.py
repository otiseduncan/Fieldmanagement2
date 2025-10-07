from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict


class ClientBase(BaseModel):
    name: str
    primary_contact: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class ClientCreate(ClientBase):
    metadata: dict[str, Any] = Field(default_factory=dict)


class ClientUpdate(BaseModel):
    primary_contact: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class ClientOut(ClientBase):
    id: int
    # Read from ORM attribute 'meta' but serialize as 'metadata'
    metadata: dict[str, Any] = Field(validation_alias='meta', serialization_alias='metadata')

    model_config = ConfigDict(from_attributes=True)
