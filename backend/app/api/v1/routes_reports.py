from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.database.session import get_db
from app.models.job import Job
from app.schemas.user import UserOut
from app.services.report_generator import generate_job_report

router = APIRouter()


@router.get('/{job_id}/export', response_class=PlainTextResponse)
async def export_job_report(
    job_id: int,
    db: Session = Depends(get_db),
    _: UserOut = Depends(get_current_active_user),
) -> str:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    return generate_job_report(job)
