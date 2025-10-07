from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import authenticate_user, create_access_token
from app.schemas.auth import Token

router = APIRouter()


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """Authenticate a user and return a JWT access token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    expires = timedelta(minutes=settings.access_token_expire_minutes)
    token = create_access_token(
        subject=user['email'],
        expires_delta=expires,
        extra={'roles': user['roles']},
    )
    return Token(access_token=token, token_type='bearer')
