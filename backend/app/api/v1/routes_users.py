from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.core.security import get_current_active_user
from app.schemas.user import UserOut

router = APIRouter()


@router.get('/me', response_model=UserOut)
async def read_current_user(current_user: UserOut = Depends(get_current_active_user)) -> UserOut:
    return current_user


@router.get('/', response_model=List[UserOut])
async def list_users(current_user: UserOut = Depends(get_current_active_user)) -> List[UserOut]:
    if 'admin' not in current_user.roles:
        return [current_user]
    # Placeholder: extend with real persistence logic
    return [current_user]
