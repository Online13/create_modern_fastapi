from fastapi import APIRouter

from src.presentation.entities.response import Response
from src.presentation.error.error_handler import create_error_response

router = APIRouter(tags=["Health Check"])


class HealthCheckResponse(Response[None]):
    pass

@router.get(
    "/health",
    response_model=HealthCheckResponse,
    responses=create_error_response("InternalServerError"),
)
async def health_check():
    return HealthCheckResponse(success=True, message="API is healthy", data=None)
