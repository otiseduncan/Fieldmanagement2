from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.gcp_client import upload_stream_to_bucket
from app.core.security import get_current_active_user
from app.database.session import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobOut, JobUpdate
from app.schemas.user import UserOut

router = APIRouter()


@router.get('/', response_model=List[JobOut])
async def list_jobs(
    *,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> List[JobOut]:
    return db.query(Job).all()


@router.post('/', response_model=JobOut, status_code=status.HTTP_201_CREATED)
async def create_job(
    *,
    job_in: JobCreate,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> JobOut:
    job = Job(**job_in.model_dump())
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
    for field, value in update_data.items():
        setattr(job, field, value)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.delete('/{job_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> None:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    db.delete(job)
    db.commit()


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

    metadata = dict(job.metadata or {})
    assets = list(metadata.get('assets', []))
    assets.append(uri)
    metadata['assets'] = assets
    job.metadata = metadata

    db.add(job)
    db.commit()
    db.refresh(job)

    return {'uri': uri}
