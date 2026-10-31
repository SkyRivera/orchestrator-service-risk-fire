from pydantic import BaseModel, Field, UUID4
from typing import Optional

class EvaluationRequest(BaseModel):
    """Petición para evaluar riesgo de incendio."""
    device_id: str = Field(..., max_length=64, description="ID de la estación ESP32")
    
    # Opción A: IDs explícitos (si el frontend ya subió las fotos)
    nubosity_image_id: Optional[UUID4] = Field(None, description="ID de imagen de cielo")
    vegetation_image_id: Optional[UUID4] = Field(None, description="ID de imagen de vegetación")
    
    # Opción B: El orquestador busca por device_id (origin_id)
    
    correlation_id: Optional[UUID4] = Field(default=None, description="ID de trazabilidad")