from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    roles = Column(JSONB, nullable=False, default=list)
    is_active = Column(Boolean, default=True)

    jobs = relationship('Job', back_populates='technician', cascade='all,delete')
