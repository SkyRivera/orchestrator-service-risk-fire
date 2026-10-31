from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories.rule_repository import RuleRepository
from app.infrastructure.persistence.repositories.audit_repository import AuditRepository
from app.infrastructure.http.media_client import MediaClient
from app.infrastructure.http.nubosity_client import NubosityClient
from app.infrastructure.http.vegetation_client import VegetationClient
from app.infrastructure.http.telemetry_client import TelemetryClient
from app.infrastructure.http.risk_fire_client import RiskFireClient
from app.application.services.rule_engine import RuleEngine
from app.application.services.orchestrator import OrchestratorService
from app.core.cache import MemoryCache

_cache = MemoryCache(max_size=1000)

def get_cache() -> MemoryCache:
    return _cache

async def get_rule_repository(db: AsyncSession = Depends(get_db), cache: MemoryCache = Depends(get_cache)) -> RuleRepository:
    return RuleRepository(db, cache)

async def get_audit_repository(db: AsyncSession = Depends(get_db)) -> AuditRepository:
    return AuditRepository(db)

async def get_rule_engine(rule_repo: RuleRepository = Depends(get_rule_repository)) -> RuleEngine:
    return RuleEngine(rule_repo)

async def get_orchestrator_service(
    rule_engine: RuleEngine = Depends(get_rule_engine),
    audit_repo: AuditRepository = Depends(get_audit_repository)
) -> OrchestratorService:
    return OrchestratorService(
        media_client=MediaClient(), nubosity_client=NubosityClient(),
        vegetation_client=VegetationClient(), telemetry_client=TelemetryClient(),
        risk_fire_client=RiskFireClient(), rule_engine=rule_engine, audit_repository=audit_repo
    )