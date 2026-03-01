from dataclasses import dataclass
from typing import Dict, List, TypeVar, Generic

from pydantic import BaseModel

Data = TypeVar("Data")


@dataclass(frozen=True)
class Response(BaseModel, Generic[Data]):
    success: bool
    message: str
    data: Data


class PaginationMetadata(BaseModel):
    total: int
    limit: int
    offset: int


class PaginatedResponse(BaseModel, Generic[Data]):
    success: bool
    message: str
    data: Data
    meta: PaginationMetadata


class ErrorBaseResponse(BaseModel):
    success: bool = False
    message: str


class BadRequestErrorResponse(ErrorBaseResponse):
    pass


class ValidationErrorResponse(ErrorBaseResponse):
    errors: Dict[str, List[str]]


class NotFoundErrorResponse(ErrorBaseResponse):
    pass


class UnauthorizedErrorResponse(ErrorBaseResponse):
    pass


class ForbiddenErrorResponse(ErrorBaseResponse):
    pass


class ConflictErrorResponse(ErrorBaseResponse):
    pass


class InternalServerErrorResponse(ErrorBaseResponse):
    pass
