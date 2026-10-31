from app.infrastructure.http.base_client import BaseHTTPClient
from app.application.dtos.external_apis import TelemetryLatestResponse
from app.core.config import settings

class TelemetryClient(BaseHTTPClient):
    def __init__(self):
        api_key = settings.TELEMETRY_API_KEY.get_secret_value() if settings.TELEMETRY_API_KEY else None
        super().__init__(base_url=settings.TELEMETRY_API_URL, api_key=api_key)

    async def get_latest(self, device_id: str) -> TelemetryLatestResponse:
        endpoint = f"/api/v1/stations/{device_id}/telemetry/latest"
        response = await self.get(endpoint)
        return TelemetryLatestResponse.model_validate(response.json())