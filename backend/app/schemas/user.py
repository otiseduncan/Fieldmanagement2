from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    roles: List[str] = Field(default_factory=list)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    roles: Optional[List[str]] = None
    is_active: Optional[bool] = None


class UserOut(UserBase):
    id: Optional[int] = None
    is_active: bool = True


class UserInDB(UserOut):
    hashed_password: str
