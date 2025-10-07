from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.database.base import Base


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    ro_number = Column(String(64), nullable=False, index=True)
    vin = Column(String(17), nullable=False, index=True)
    status = Column(String(32), nullable=False, default='pending')
    technician_notes = Column(Text, nullable=True)
    client_notes = Column(Text, nullable=True)
    metadata = Column(JSONB, nullable=False, default=dict)
    amount = Column(Numeric(10, 2), nullable=True)

    scheduled_start = Column(DateTime, nullable=True)
    scheduled_end = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    technician_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)

    technician = relationship('User', back_populates='jobs')
    client = relationship('Client', back_populates='jobs')
