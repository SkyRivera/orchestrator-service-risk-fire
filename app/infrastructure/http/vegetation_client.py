from app.infrastructure.http.base_client import BaseHTTPClient
from app.application.dtos.external_apis import VegetationResponse
from app.core.config import settings

class VegetationClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(base_url=settings.VEGETATION_API_URL)

    async def predict(self, image_bytes: bytes, filename: str) -> VegetationResponse:
        files = {"image": (filename, image_bytes, "image/jpeg")}
        response = await self.post("/api/v1/vegetation/predict", files=files)
        return VegetationResponse.model_validate(response.json())