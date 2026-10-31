from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime

class RuleEvaluationResult(BaseModel):
    estatus: str
    semaforo: str
    monitoreo: str
    medidas: str
    vigilancia: str
    prevencion: str

class OrchestratorResponse(BaseModel):
    evaluation_id: UUID
    timestamp: datetime
    risk_technical: Dict[str, Any]
    rule_evaluation: RuleEvaluationResult
    correlation_id: Optional[UUID] = None