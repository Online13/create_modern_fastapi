from fastapi import APIRouter

from src.presentation.core.error_handler import create_error_response
from src.presentation.schemas.app import HealthCheckResponse


router = APIRouter(tags=["App"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    responses=create_error_response("InternalServerError"),
)
async def health_check():
    return {"success": True, "message": "API is healthy"}
