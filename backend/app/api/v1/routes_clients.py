from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.database.session import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.schemas.user import UserOut

router = APIRouter()


@router.get('/', response_model=List[ClientOut])
async def list_clients(
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> List[ClientOut]:
    return db.query(Client).order_by(Client.name).all()


@router.post('/', response_model=ClientOut, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> ClientOut:
    client = Client(**client_in.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get('/{client_id}', response_model=ClientOut)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> ClientOut:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Client not found')
    return client


@router.patch('/{client_id}', response_model=ClientOut)
async def update_client(
    client_id: int,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> ClientOut:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Client not found')
    update_data = client_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.delete('/{client_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> None:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Client not found')
    db.delete(client)
    db.commit()
