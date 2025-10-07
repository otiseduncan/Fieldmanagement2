from app.database.base import Base
from app.database.session import engine
from app.models import client, job, user  # noqa: F401


def init_db() -> None:
    """Create database tables based on the SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)
