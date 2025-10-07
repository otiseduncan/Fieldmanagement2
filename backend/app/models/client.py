from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.database.base import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    primary_contact = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(32), nullable=True)
    address = Column(Text, nullable=True)
    metadata = Column(JSONB, nullable=False, default=dict)

    jobs = relationship('Job', back_populates='client', cascade='all,delete')
