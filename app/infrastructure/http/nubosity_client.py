from app.infrastructure.http.base_client import BaseHTTPClient
from app.application.dtos.external_apis import NubosityResponse
from app.core.config import settings

class NubosityClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(base_url=settings.NUBOSITY_API_URL)

    async def predict(self, image_bytes: bytes, filename: str) -> NubosityResponse:
        files = {"file": (filename, image_bytes, "image/jpeg")}
        response = await self.post("/api/v1/nubosity/predict", files=files)
        return NubosityResponse.model_validate(response.json())