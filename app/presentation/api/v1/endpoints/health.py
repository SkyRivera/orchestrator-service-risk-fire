from fastapi import APIRouter, status
from datetime import datetime
from app.core.config import settings

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK, summary="Health check")
async def health_check():
    return {
        "status": "healthy", "service": settings.APP_NAME,
        "version": settings.APP_VERSION, "timestamp": datetime.utcnow().isoformat() + "Z"
    }