import httpx
import asyncio
import logging
from typing import Optional, Dict
from app.core.config import settings
from app.core.exceptions import ExternalAPIError, ExternalAPITimeoutError

logger = logging.getLogger(__name__)

class BaseHTTPClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: Optional[httpx.Timeout] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout or httpx.Timeout(
            connect=settings.HTTP_TIMEOUT_CONNECT,
            read=settings.HTTP_TIMEOUT_READ,
            write=settings.HTTP_TIMEOUT_READ,
            pool=settings.HTTP_TIMEOUT_CONNECT
        )
        self.max_retries = settings.HTTP_MAX_RETRIES
        self.backoff = settings.HTTP_RETRY_BACKOFF

    def _get_headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        if extra:
            headers.update(extra)
        return headers

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers(kwargs.pop("headers", None))
        
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(method, url, headers=headers, **kwargs)
                    response.raise_for_status()
                    return response
            except httpx.TimeoutException as e:
                last_exception = e
                logger.warning(f"Timeout en {url} (intento {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.backoff * (2 ** attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    last_exception = e
                    logger.warning(f"Rate limit en {url} (intento {attempt + 1}/{self.max_retries})")
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.backoff * (2 ** attempt))
                else:
                    raise ExternalAPIError(
                        f"Error HTTP {e.response.status_code} en {url}: {e.response.text}",
                        status_code=e.response.status_code
                    ) from e
            except httpx.RequestError as e:
                last_exception = e
                logger.warning(f"Error de conexión en {url}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.backoff * (2 ** attempt))
        
        if isinstance(last_exception, httpx.TimeoutException):
            raise ExternalAPITimeoutError(f"Timeout en {url} tras {self.max_retries} intentos")
        raise ExternalAPIError(f"Error en {url}: {last_exception}")

    async def get(self, endpoint: str, **kwargs) -> httpx.Response:
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> httpx.Response:
        return await self._request("POST", endpoint, **kwargs)