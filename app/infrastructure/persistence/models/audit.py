from sqlalchemy import Column, String, Float, DateTime, JSON, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase
import uuid

class Base(DeclarativeBase):
    pass

class AuditEvaluation(Base):
    __tablename__ = "audit_evaluations"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    correlation_id = Column(PG_UUID(as_uuid=True), nullable=True, index=True)
    device_id = Column(String(64), nullable=False, index=True)
    input_data = Column(JSON, nullable=False)
    nubosity_response = Column(JSON, nullable=True)
    vegetation_response = Column(JSON, nullable=True)
    telemetry_response = Column(JSON, nullable=True)
    risk_fire_response = Column(JSON, nullable=True)
    rule_evaluation = Column(JSON, nullable=True)
    status = Column(String(20), nullable=False, default="success")
    error_message = Column(String(500), nullable=True)
    processing_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)