import asyncio
import fnmatch
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MemoryCache:
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, tuple[Any, Optional[datetime]]] = {}
        self._max_size = max_size
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if expiry is None or expiry > datetime.utcnow():
                    return value
                else:
                    del self._cache[key]
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        async with self._lock:
            if len(self._cache) >= self._max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            expiry = datetime.utcnow() + timedelta(seconds=ttl) if ttl else None
            self._cache[key] = (value, expiry)

    async def clear_pattern(self, pattern: str) -> None:
        async with self._lock:
            keys_to_delete = [k for k in self._cache if fnmatch.fnmatch(k, pattern)]
            for k in keys_to_delete:
                del self._cache[k]