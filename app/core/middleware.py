from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import uuid

logger = logging.getLogger(__name__)

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        logger.info(f"[{correlation_id}] {request.method} {request.url.path}")
        response: Response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response