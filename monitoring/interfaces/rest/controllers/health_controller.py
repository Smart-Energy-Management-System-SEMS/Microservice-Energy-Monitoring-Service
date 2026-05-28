from datetime import datetime
from fastapi import APIRouter
from monitoring.interfaces.rest.resources.health_resource import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse, summary="Health check")
async def health_check() -> HealthResponse:
    """Returns the health status of the Energy Monitoring Service."""
    return HealthResponse(
        status="ok",
        service="Microservice-Energy-Monitoring-Service",
        version="1.0.0",
        timestamp=datetime.utcnow(),
    )
