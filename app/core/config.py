from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    APP_NAME: str = "orchestrator-service"
    APP_VERSION: str = "1.1.0"
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    LOG_LEVEL: str = "INFO"

    # Base de Datos
    DATABASE_URL: SecretStr = Field(..., description="PostgreSQL async URL")
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False

    # APIs Externas
    MEDIA_API_URL: str = Field(..., description="URL base de media-api")
    MEDIA_API_KEY: Optional[SecretStr] = None
    
    NUBOSITY_API_URL: str = Field(..., description="URL base de nubosity_api")
    VEGETATION_API_URL: str = Field(..., description="URL base de vegetation-api")
    TELEMETRY_API_URL: str = Field(..., description="URL base de telemetry-api")
    RISK_FIRE_API_URL: str = Field(..., description="URL base de risk-fire-monitoring-api")

    TELEMETRY_API_KEY: Optional[SecretStr] = None
    #RISK_FIRE_API_KEY: Optional[SecretStr] = None

    # HTTP Client
    HTTP_TIMEOUT_CONNECT: float = 5.0
    HTTP_TIMEOUT_READ: float = 30.0
    HTTP_MAX_RETRIES: int = 3
    HTTP_RETRY_BACKOFF: float = 0.5

    # Caché de Reglas
    RULE_CACHE_TTL_SECONDS: int = 300
    RULE_CACHE_MAX_SIZE: int = 100

settings = Settings()