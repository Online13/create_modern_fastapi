
from pydantic import BaseModel


class ErrorBaseResponse(BaseModel):
    success: bool = False
    message: str


class BadRequestErrorResponse(ErrorBaseResponse):
    pass


class ValidationErrorResponse(ErrorBaseResponse):
    errors: dict[str, list[str]]


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
