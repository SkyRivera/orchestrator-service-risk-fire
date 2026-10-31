from sqlalchemy import Column, String, DateTime, Boolean, Integer, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from .audit import Base

class RiskRule(Base):
    __tablename__ = "risk_rules"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_category = Column(String(50), nullable=False, unique=True, index=True)
    estatus = Column(String(100), nullable=False)
    semaforo = Column(String(50), nullable=False)
    monitoreo = Column(String(200), nullable=False)
    medidas = Column(String(500), nullable=False)
    vigilancia = Column(String(200), nullable=False)
    prevencion = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)