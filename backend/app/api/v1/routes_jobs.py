from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.gcp_client import upload_stream_to_bucket
from app.core.security import get_current_active_user
from app.database.session import get_db
from app.models.job import Job
from app.models.client import Client
from app.models.user import User
from app.schemas.job import JobCreate, JobOut, JobUpdate
from app.schemas.user import UserOut

router = APIRouter()


@router.get('/', response_model=List[JobOut])
@router.get('', response_model=List[JobOut])
async def list_jobs(
    *,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> List[JobOut]:
    return db.query(Job).all()


@router.post('/', response_model=JobOut, status_code=status.HTTP_201_CREATED)
@router.post('', response_model=JobOut, status_code=status.HTTP_201_CREATED)
async def create_job(
    *,
    job_in: JobCreate,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> JobOut:
    data = job_in.model_dump()
    if 'metadata' in data:
        data['meta'] = data.pop('metadata')
    job = Job(**data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get('/{job_id}', response_model=JobOut)
async def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> JobOut:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    return job


@router.patch('/{job_id}', response_model=JobOut)
async def update_job(
    job_id: int,
    job_in: JobUpdate,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> JobOut:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    update_data = job_in.model_dump(exclude_unset=True)
    if 'metadata' in update_data:
        update_data['meta'] = update_data.pop('metadata')
    for field, value in update_data.items():
        setattr(job, field, value)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.delete(
    '/{job_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> Response:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    db.delete(job)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/upload', status_code=status.HTTP_201_CREATED)
async def upload_job_asset(
    job_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> dict[str, str]:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')

    destination = f'jobs/{job_id}/{file.filename}'
    file.file.seek(0)
    uri = upload_stream_to_bucket(
        bucket_name=settings.gcs_bucket,
        stream=file.file,
        destination=destination,
        content_type=file.content_type or 'application/octet-stream',
    )

    metadata = dict((job.meta or {}))
    assets = list(metadata.get('assets', []))
    assets.append(uri)
    metadata['assets'] = assets
    job.meta = metadata

    db.add(job)
    db.commit()
    db.refresh(job)

    return {'uri': uri}


@router.post('/_seed', response_model=List[JobOut])
async def seed_jobs(
    *,
    count: int = 8,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_active_user),
) -> List[JobOut]:
    """Seed demo jobs and a demo client for local testing (admin only)."""
    if 'admin' not in (current_user.roles or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin only')

    # Ensure a demo client exists
    client = db.query(Client).filter(Client.name == 'Demo Client').first()
    if client is None:
        client = Client(name='Demo Client', primary_contact='Demo Owner', email='owner@demo.example')
        db.add(client)
        db.flush()

    # Try to find a technician user for assignment
    tech = db.query(User).filter(User.email == 'tech@example.com').first()
    tech_id = tech.id if tech else None

    statuses = ['pending', 'assigned', 'in_progress', 'completed']
    created: list[Job] = []
    base_num = (db.query(Job).count() or 0) + 3000
    for i in range(count):
        status = statuses[i % len(statuses)]
        job = Job(
            ro_number=f'RO-{base_num + i}',
            vin=f'1HGCM82633A{(123450 + i):06d}',
            status=status,
            client_notes='Demo seeded job',
            technician_id=tech_id if status in {'assigned', 'in_progress', 'completed'} else None,
            client_id=client.id,
            meta={'region': ['north', 'south', 'east', 'west'][i % 4], 'service_type': 'calibration'},
        )
        db.add(job)
        created.append(job)

    db.commit()
    for j in created:
        db.refresh(j)
    return created
