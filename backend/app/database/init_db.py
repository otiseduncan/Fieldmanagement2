from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import client, job, user  # noqa: F401
from app.models.client import Client
from app.models.job import Job
from app.models.user import User


def init_db() -> None:
    """Create database tables based on the SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


def seed_demo_data(count: int = 12) -> None:
    """Seed demo client and jobs for local/dev environments.

    Runs only if there are currently no jobs to avoid duplicating on restarts.
    """
    db: Session = SessionLocal()
    try:
        existing_jobs = db.query(Job).count()
        if existing_jobs > 0:
            return

        # Ensure a demo client exists
        demo = db.query(Client).filter(Client.name == 'Demo Client').first()
        if demo is None:
            demo = Client(name='Demo Client', primary_contact='Demo Owner', email='owner@demo.example')
            db.add(demo)
            db.flush()

        # Try to locate a technician for assignment (optional)
        tech = db.query(User).filter(User.email == 'tech@example.com').first()
        tech_id = tech.id if tech else None

        statuses = ['pending', 'assigned', 'in_progress', 'completed']
        base_num = 4000
        for i in range(count):
            status = statuses[i % len(statuses)]
            j = Job(
                ro_number=f'RO-{base_num + i}',
                vin=f'1HGCM82633A{(223450 + i):06d}',
                status=status,
                client_notes='Demo seeded job',
                technician_id=tech_id if status in {'assigned', 'in_progress', 'completed'} else None,
                client_id=demo.id,
                meta={'region': ['north', 'south', 'east', 'west'][i % 4], 'service_type': 'calibration'},
            )
            db.add(j)

        db.commit()
    finally:
        db.close()

