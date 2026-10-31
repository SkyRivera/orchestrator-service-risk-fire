from fastapi import APIRouter
from app.presentation.api.v1.endpoints import evaluate, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(evaluate.router, prefix="/orchestrator", tags=["orchestrator"])