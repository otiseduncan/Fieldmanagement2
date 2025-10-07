from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    roles: list[str] = []
    iat: Optional[int] = None
    nbf: Optional[int] = None
    iss: Optional[str] = None
    aud: Optional[str] = None
    jti: Optional[str] = None
    scopes: list[str] = []


class RefreshToken(BaseModel):
    token: str
    expires_at: datetime
