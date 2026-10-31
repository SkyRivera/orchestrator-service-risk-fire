import asyncio
import time
import logging
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from app.application.dtos.external_apis import RiskFireRequest
from app.application.dtos.responses import OrchestratorResponse
from app.application.services.rule_engine import RuleEngine
from app.infrastructure.http.media_client import MediaClient
from app.infrastructure.http.nubosity_client import NubosityClient
from app.infrastructure.http.vegetation_client import VegetationClient
from app.infrastructure.http.telemetry_client import TelemetryClient
from app.infrastructure.http.risk_fire_client import RiskFireClient
from app.infrastructure.persistence.repositories.audit_repository import AuditRepository
from app.core.exceptions import ExternalAPIError, PartialFailureError, RuleNotFoundError

logger = logging.getLogger(__name__)

class OrchestratorService:
    def __init__(
        self, media_client: MediaClient, nubosity_client: NubosityClient,
        vegetation_client: VegetationClient, telemetry_client: TelemetryClient,
        risk_fire_client: RiskFireClient, rule_engine: RuleEngine,
        audit_repository: AuditRepository
    ):
        self.media_client = media_client
        self.nubosity_client = nubosity_client
        self.vegetation_client = vegetation_client
        self.telemetry_client = telemetry_client
        self.risk_fire_client = risk_fire_client
        self.rule_engine = rule_engine
        self.audit_repository = audit_repository

    async def evaluate_risk(
        self, device_id: str, nubosity_image_id: Optional[str] = None,
        vegetation_image_id: Optional[str] = None, correlation_id: Optional[UUID] = None
    ) -> OrchestratorResponse:
        
        start_time = time.perf_counter()
        evaluation_id = uuid4()
        correlation_id = correlation_id or uuid4()
        logger.info(f"[{correlation_id}] Iniciando evaluación para device_id={device_id}")

        # FASE 0: Obtener imágenes (Media API)
        try:
            if nubosity_image_id and vegetation_image_id:
                logger.info(f"[{correlation_id}] Obteniendo imágenes por ID explícito...")
                nubosity_bytes, nubosity_filename = await self.media_client.get_image_content_by_id(nubosity_image_id)
                vegetation_bytes, vegetation_filename = await self.media_client.get_image_content_by_id(vegetation_image_id)
            else:
                logger.info(f"[{correlation_id}] Buscando últimas imágenes para origin_id={device_id}...")
                nub_task = self.media_client.get_image_by_metadata(device_id, "cielo")
                veg_task = self.media_client.get_image_by_metadata(device_id, "vegetacion")
                (nubosity_bytes, nubosity_filename), (vegetation_bytes, vegetation_filename) = await asyncio.gather(nub_task, veg_task)
        except ExternalAPIError as e:
            logger.error(f"[{correlation_id}] Error obteniendo imágenes: {e}")
            raise e

        # FASE 1: Consultas concurrentes
        nubosity_task = self._safe_call(self.nubosity_client.predict(nubosity_bytes, nubosity_filename), "nubosity_api")
        vegetation_task = self._safe_call(self.vegetation_client.predict(vegetation_bytes, vegetation_filename), "vegetation-api")
        telemetry_task = self._safe_call(self.telemetry_client.get_latest(device_id), "telemetry-api")
        
        results = await asyncio.gather(nubosity_task, vegetation_task, telemetry_task, return_exceptions=True)
        nubosity_resp, vegetation_resp, telemetry_resp = results
        
        # FASE 2: Validar resultados
        errors = []
        if isinstance(nubosity_resp, Exception): errors.append(f"nubosity: {nubosity_resp}")
        if isinstance(vegetation_resp, Exception): errors.append(f"vegetation: {vegetation_resp}")
        if isinstance(telemetry_resp, Exception): errors.append(f"telemetry: {telemetry_resp}")
        
        if errors:
            error_msg = "; ".join(errors)
            await self._audit_failure(evaluation_id, correlation_id, device_id, error_msg, start_time)
            raise PartialFailureError(f"Fallos en APIs: {error_msg}")
        
        # FASE 3: Transformar y Risk Fire
        try:
            risk_request = self._transform_to_risk_request(nubosity_resp, vegetation_resp, telemetry_resp)
            risk_response = await self.risk_fire_client.predict(risk_request)
        except ExternalAPIError as e:
            await self._audit_failure(evaluation_id, correlation_id, device_id, str(e), start_time)
            raise
        
        # FASE 4: Evaluar Reglas
        try:
            rule_result = await self.rule_engine.evaluate(risk_response.prediction.category)
        except RuleNotFoundError as e:
            await self._audit_failure(evaluation_id, correlation_id, device_id, str(e), start_time)
            raise
        
        # --- FASE 5: Auditoría Exitosa ---
        processing_time_ms = (time.perf_counter() - start_time) * 1000
        await self.audit_repository.create_success_audit(
            evaluation_id=evaluation_id, 
            correlation_id=correlation_id, 
            device_id=device_id,
            input_data={"nubosity_id": nubosity_image_id, "vegetation_id": vegetation_image_id},
            
            # Agregar mode="json" aquí:
            nubosity_response=nubosity_resp.model_dump(mode="json"), 
            vegetation_response=vegetation_resp.model_dump(mode="json"),
            telemetry_response=telemetry_resp.model_dump(mode="json"), 
            risk_fire_response=risk_response.model_dump(mode="json"),
            rule_evaluation=rule_result.model_dump(mode="json"), 
            
            processing_time_ms=processing_time_ms
        )
        
        return OrchestratorResponse(
            evaluation_id=evaluation_id, timestamp=datetime.utcnow(),
            risk_technical=risk_response.model_dump(), rule_evaluation=rule_result, correlation_id=correlation_id
        )

    async def _safe_call(self, coro, api_name: str):
        try:
            return await coro
        except Exception as e:
            logger.warning(f"Error en {api_name}: {e}")
            return e

    def _transform_to_risk_request(self, nubosity, vegetation, telemetry) -> RiskFireRequest:
        # Mapeo crítico por el typo en el contrato de risk-fire
        veg_map = {
            "semi_humeda": "semi-humeda", "seca": "seca",
            "muy_seca": "muy_seca", "muy_seca_extrema": "muy_sea_extrema"
        }
        sky_map = {
            "nublado": "nublado", "medio_nublado": "medio_nublado",
            "soleado": "soleado", "soleado_extremo": "soleado_extremo"
        }
        # Fallbacks si la telemetría falla en algún sensor (None)
        return RiskFireRequest(
            temperatura=telemetry.temperature if telemetry.temperature is not None else 25.0,
            humedad=telemetry.humidity if telemetry.humidity is not None else 50.0,
            viento=telemetry.wind_speed_kwh if telemetry.wind_speed_kwh is not None else 0.0,
            vegetacion=veg_map.get(vegetation.prediction.category, "seca"),
            cielo=sky_map.get(nubosity.category, "soleado")
        )

    async def _audit_failure(self, eval_id, corr_id, device_id, error_msg, start_time):
        proc_time = (time.perf_counter() - start_time) * 1000
        await self.audit_repository.create_failure_audit(
            evaluation_id=eval_id, correlation_id=corr_id, device_id=device_id,
            input_data={"device_id": device_id}, nubosity_response=None,
            vegetation_response=None, telemetry_response=None,
            error_message=error_msg[:500], processing_time_ms=proc_time
        )