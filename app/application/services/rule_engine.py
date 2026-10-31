from app.infrastructure.persistence.repositories.rule_repository import RuleRepository
from app.application.dtos.responses import RuleEvaluationResult
from app.core.exceptions import RuleNotFoundError
import logging

logger = logging.getLogger(__name__)

class RuleEngine:
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository

    async def evaluate(self, risk_category: str) -> RuleEvaluationResult:
        rule = await self.rule_repository.get_rule_by_category(risk_category)
        if not rule:
            logger.error(f"No se encontró regla para categoría: {risk_category}")
            raise RuleNotFoundError(f"No hay regla definida para la categoría: {risk_category}")
        
        return RuleEvaluationResult(
            estatus=rule.estatus,
            semaforo=rule.semaforo,
            monitoreo=rule.monitoreo,
            medidas=rule.medidas,
            vigilancia=rule.vigilancia,
            prevencion=rule.prevencion
        )