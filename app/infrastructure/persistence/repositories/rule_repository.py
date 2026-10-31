from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.models.rule import RiskRule
from app.core.cache import MemoryCache
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RuleRepository:
    def __init__(self, session: AsyncSession, cache: MemoryCache):
        self.session = session
        self.cache = cache

    async def get_rule_by_category(self, risk_category: str) -> Optional[RiskRule]:
        cache_key = f"rule:{risk_category}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        stmt = select(RiskRule).where(RiskRule.risk_category == risk_category, RiskRule.is_active == True)
        result = await self.session.execute(stmt)
        rule = result.scalar_one_or_none()
        
        if rule:
            await self.cache.set(cache_key, rule, ttl=settings.RULE_CACHE_TTL_SECONDS)
        return rule