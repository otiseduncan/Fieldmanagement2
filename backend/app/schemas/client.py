from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field


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
    metadata: dict[str, Any]

    class Config:
        orm_mode = True
