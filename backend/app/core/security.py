from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.user import UserInDB, UserOut

# Use PBKDF2 for local/dev auth to avoid bcrypt backend constraints in containers.
pwd_context = CryptContext(
    schemes=['pbkdf2_sha256'],
    deprecated='auto',
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

_fake_users_db: Dict[str, Dict[str, Any]] = {
    'admin@example.com': {
        'id': 1,
        'email': 'admin@example.com',
        'full_name': 'Admin User',
        'roles': ['admin'],
        'is_active': True,
        'hashed_password': '',
    },
    'tech@example.com': {
        'id': 2,
        'email': 'tech@example.com',
        'full_name': 'Technician User',
        'roles': ['technician'],
        'is_active': True,
        'hashed_password': '',
    },
    'cmr@example.com': {
        'id': 3,
        'email': 'cmr@example.com',
        'full_name': 'CMR User',
        'roles': ['cmr'],
        'is_active': True,
        'hashed_password': '',
    },
    'client@example.com': {
        'id': 4,
        'email': 'client@example.com',
        'full_name': 'Client User',
        'roles': ['client'],
        'is_active': True,
        'hashed_password': '',
    },
}

# Initialize fake users' password hashes at import time
_fake_users_db['admin@example.com']['hashed_password'] = pwd_context.hash('admin123')
_fake_users_db['tech@example.com']['hashed_password'] = pwd_context.hash('tech123')
_fake_users_db['cmr@example.com']['hashed_password'] = pwd_context.hash('cmr123')
_fake_users_db['client@example.com']['hashed_password'] = pwd_context.hash('client123')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(email: str) -> UserInDB | None:
    data = _fake_users_db.get(email.lower())
    if not data:
        return None
    return UserInDB(**data)


def authenticate_user(username: str, password: str) -> UserOut | None:
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return UserOut(**user.model_dump(exclude={'hashed_password'}))


def create_access_token(
    *,
    subject: str,
    expires_delta: timedelta | None = None,
    extra: Dict[str, Any] | None = None,
) -> str:
    to_encode: Dict[str, Any] = extra.copy() if extra else {}
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({'sub': subject, 'exp': expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        subject: str | None = payload.get('sub')
        if subject is None:
            raise credentials_exception
    except JWTError as exc:  # noqa: PERF203
        raise credentials_exception from exc

    user = get_user(subject)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return UserOut(**user.model_dump(exclude={'hashed_password'}))


async def get_current_active_user(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
