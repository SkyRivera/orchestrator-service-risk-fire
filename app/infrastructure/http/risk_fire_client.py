from app.infrastructure.http.base_client import BaseHTTPClient
from app.application.dtos.external_apis import RiskFireRequest, RiskFireResponse
from app.core.config import settings

class RiskFireClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(base_url=settings.RISK_FIRE_API_URL)

    async def predict(self, payload: RiskFireRequest) -> RiskFireResponse:
        response = await self.post("/api/v1/risk/predict", json=payload.model_dump())
        return RiskFireResponse.model_validate(response.json())