from pydantic import BaseModel
from src.presentation.schemas.core import Response


class HealthCheckResponse(Response[None]):
    pass
