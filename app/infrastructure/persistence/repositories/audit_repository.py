from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.models.audit import AuditEvaluation
from typing import Optional, Dict, Any
from uuid import UUID

class AuditRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_success_audit(
        self, evaluation_id: UUID, correlation_id: UUID, device_id: str,
        input_data: Dict[str, Any], nubosity_response: Dict[str, Any],
        vegetation_response: Dict[str, Any], telemetry_response: Dict[str, Any],
        risk_fire_response: Dict[str, Any], rule_evaluation: Dict[str, Any],
        processing_time_ms: float
    ) -> AuditEvaluation:
        audit = AuditEvaluation(
            id=evaluation_id, correlation_id=correlation_id, device_id=device_id,
            input_data=input_data, nubosity_response=nubosity_response,
            vegetation_response=vegetation_response, telemetry_response=telemetry_response,
            risk_fire_response=risk_fire_response, rule_evaluation=rule_evaluation,
            status="success", processing_time_ms=processing_time_ms
        )
        self.session.add(audit)
        await self.session.commit()
        return audit

    async def create_failure_audit(
        self, evaluation_id: UUID, correlation_id: UUID, device_id: str,
        input_data: Dict[str, Any], nubosity_response: Optional[Dict[str, Any]],
        vegetation_response: Optional[Dict[str, Any]], telemetry_response: Optional[Dict[str, Any]],
        error_message: str, processing_time_ms: float, status: str = "error"
    ) -> AuditEvaluation:
        audit = AuditEvaluation(
            id=evaluation_id, correlation_id=correlation_id, device_id=device_id,
            input_data=input_data, nubosity_response=nubosity_response,
            vegetation_response=vegetation_response, telemetry_response=telemetry_response,
            status=status, error_message=error_message, processing_time_ms=processing_time_ms
        )
        self.session.add(audit)
        await self.session.commit()
        return audit