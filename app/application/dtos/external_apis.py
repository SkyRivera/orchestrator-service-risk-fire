from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# --- Nubosity API ---
class NubosityResponse(BaseModel):
    prediction_id: UUID
    timestamp: datetime
    model_name: str
    model_version: str
    category: str
    confidence: float
    distribution: Dict[str, float]

# --- Vegetation API ---
class VegetationPredictionDetail(BaseModel):
    category: str
    confidence: float

class VegetationResponse(BaseModel):
    prediction_id: UUID
    timestamp: datetime
    model: Dict[str, Any]
    prediction: VegetationPredictionDetail
    distribution: Dict[str, float]
    features: Dict[str, float]

# --- Telemetry API ---
class TelemetryLatestResponse(BaseModel):
    device_id: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed_kwh: Optional[float] = None
    measured_at: datetime
    received_at: datetime
    reading_type: str
    sensor_status: str

# --- Risk Fire API ---
class RiskFireRequest(BaseModel):
    temperatura: float
    humedad: float
    viento: float
    vegetacion: str
    cielo: str

class RiskFirePrediction(BaseModel):
    category: str
    confidence: float

class RiskFireResponse(BaseModel):
    prediction_id: UUID
    timestamp: datetime
    model_name: str
    model_version: str
    prediction: RiskFirePrediction
    distribution: Dict[str, float]
    features: Dict[str, Any]