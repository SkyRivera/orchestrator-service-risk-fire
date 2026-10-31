from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dtos.requests import EvaluationRequest
from app.application.dtos.responses import OrchestratorResponse
from app.presentation.api.dependencies import get_orchestrator_service
from app.application.services.orchestrator import OrchestratorService
from app.core.exceptions import ExternalAPIError, PartialFailureError, RuleNotFoundError

router = APIRouter()

@router.post("/evaluate", response_model=OrchestratorResponse, status_code=status.HTTP_200_OK)
async def evaluate_risk(
    request: EvaluationRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator_service)
):
    try:
        return await orchestrator.evaluate_risk(
            device_id=request.device_id,
            nubosity_image_id=str(request.nubosity_image_id) if request.nubosity_image_id else None,
            vegetation_image_id=str(request.vegetation_image_id) if request.vegetation_image_id else None,
            correlation_id=request.correlation_id
        )
    except ExternalAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except PartialFailureError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=e.message)
    except RuleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))