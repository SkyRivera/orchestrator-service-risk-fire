import httpx
from app.infrastructure.http.base_client import BaseHTTPClient
from app.core.config import settings
from app.core.exceptions import ExternalAPIError
import logging

logger = logging.getLogger(__name__)

class MediaClient(BaseHTTPClient):
    def __init__(self):
        api_key = settings.MEDIA_API_KEY.get_secret_value() if settings.MEDIA_API_KEY else None
        super().__init__(base_url=settings.MEDIA_API_URL, api_key=api_key)

    async def get_image_by_metadata(self, origin_id: str, media_type: str) -> tuple[bytes, str]:
        """
        Busca la última imagen por origin_id y media_type, y descarga sus bytes.
        """
        endpoint = f"/api/v1/images?origin_id={origin_id}&media_type={media_type}"
        response = await self.get(endpoint)
        
        data = response.json()
        if not data.get("items"):
            raise ExternalAPIError(f"No se encontró imagen para origin={origin_id}, tipo={media_type}", status_code=404)
            
        image_metadata = data["items"][0]
        content_url = image_metadata["content_url"]
        filename = f"{media_type}_{origin_id}.jpg"

        # --- CORRECCIÓN AQUÍ ---
        # Si content_url ya es una URL absoluta (empieza con http), 
        # no debemos usar self.get() porque añadiría la base_url de nuevo.
        if content_url.startswith("http"):
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                headers = self._get_headers()
                content_response = await client.get(content_url, headers=headers)
        else:
            content_response = await self.get(content_url)
        
        if content_response.status_code != 200:
            raise ExternalAPIError(f"Error descargando imagen desde {content_url}", content_response.status_code)

        return content_response.content, filename

    async def get_image_content_by_id(self, image_id: str) -> tuple[bytes, str]:
        """Descarga el binario por ID explícito."""
        endpoint = f"/api/v1/images/{image_id}/content"
        response = await self.get(endpoint)
        return response.content, f"{image_id}.jpg"