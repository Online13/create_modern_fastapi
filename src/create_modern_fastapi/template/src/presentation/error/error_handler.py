from typing import Any, Literal, TypedDict, cast
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.presentation.error.error_schema import (
    ConflictErrorResponse,
    BadRequestErrorResponse,
    ErrorBaseResponse,
    ForbiddenErrorResponse,
    InternalServerErrorResponse,
    NotFoundErrorResponse,
    UnauthorizedErrorResponse,
    ValidationErrorResponse,
)
from src.domain.exceptions.core import (
    BadRequestException,
    ConflictException,
    DomainException,
    InternalServerErrorException,
    NotFoundException,
)
from src.domain.exceptions.auth import (
    AuthDomainException,
    InvalidCredentialsException,
    InvalidTokenException,
    TokenExpiredException,
    UnauthorizedAccessException,
)


class AppException(HTTPException):
    def __init__(
        self, status_code: int, detail: str, code: str | None = None, **kwargs: Any
    ):
        super().__init__(status_code=status_code, detail=detail, **kwargs)
        self.detail = detail
        self.code = code


def bind(app: FastAPI):

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):  # type: ignore
        print("error", exc)
        status_code = 400

        if isinstance(exc, AuthDomainException):
            status_code = status.HTTP_401_UNAUTHORIZED
            if isinstance(exc, TokenExpiredException):
                detail = "Token has expired. Please log in again."
            elif isinstance(exc, InvalidTokenException):
                detail = "Invalid token. Please log in again."
            elif isinstance(exc, UnauthorizedAccessException):
                detail = "Could not validate credentials. Please log in again."
            elif isinstance(exc, InvalidCredentialsException):
                detail = "Invalid username or password."
            elif isinstance(exc, UnauthorizedAccessException):
                detail = "Unauthorized access."
            else:
                detail = exc.message
        else:
            if isinstance(exc, NotFoundException):
                status_code = status.HTTP_404_NOT_FOUND
            elif isinstance(exc, BadRequestException):
                status_code = status.HTTP_400_BAD_REQUEST
            elif isinstance(exc, InternalServerErrorException):
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            elif isinstance(exc, ConflictException):
                status_code = status.HTTP_409_CONFLICT
            detail = exc.message

        return JSONResponse(
            status_code=status_code,
            headers=getattr(exc, "headers", None),
            content=(
                {
                    "success": False,
                    "message": detail,
                    "code": exc.code,
                }
            ),
        )

    @app.exception_handler(AppException)
    async def exception_handler(request: Request, exc: AppException):  # type: ignore
        return JSONResponse(
            status_code=exc.status_code,
            headers=getattr(exc, "headers", None),
            content=(
                {
                    "success": False,
                    "message": exc.detail,
                    "code": exc.code,
                }
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(  # type: ignore
        request: Request, exc: RequestValidationError
    ):

        errors: Any = {}
        for err in exc.errors():
            field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
            message = err["msg"]
            errors.setdefault(field, []).append(message)

        print("Validation error:", errors)
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation error",
                "errors": errors,
            },
        )


# --------------------------------------------------------------------------------

type ErrorName = Literal[
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "Conflict",
    "InvalidData",
    "InternalServerError",
]


class ErrorResponse(TypedDict):
    model: type[ErrorBaseResponse]
    description: str


class ResponseData(TypedDict):
    status: int
    response: ErrorResponse


ERROR_RESPONSES: dict[ErrorName, ResponseData] = {
    "BadRequest": {
        "status": 400,
        "response": {
            "model": BadRequestErrorResponse,
            "description": "Bad Request",
        },
    },
    "Unauthorized": {
        "status": 401,
        "response": {
            "model": UnauthorizedErrorResponse,
            "description": "Unauthorized",
        },
    },
    "Forbidden": {
        "status": 403,
        "response": {
            "model": ForbiddenErrorResponse,
            "description": "Forbidden",
        },
    },
    "NotFound": {
        "status": 404,
        "response": {
            "model": NotFoundErrorResponse,
            "description": "Not Found",
        },
    },
    "Conflict": {
        "status": 409,
        "response": {
            "model": ConflictErrorResponse,
            "description": "Conflict",
        },
    },
    "InternalServerError": {
        "status": 500,
        "response": {
            "model": InternalServerErrorResponse,
            "description": "Internal Server Error",
        },
    },
    "InvalidData": {
        "status": 422,
        "response": {
            "model": ValidationErrorResponse,
            "description": "Validation Error",
        },
    },
}


def create_error_response(
    first_error: ErrorName, *other_errors: ErrorName
) -> dict[int | str, dict[str, Any]]:
    responses: dict[int, ErrorResponse] = {}
    all_names = [first_error] + list(other_errors)

    for name in all_names:
        if name not in ERROR_RESPONSES:
            raise ValueError(f"Error name '{name}' is not defined.")

        error_data = ERROR_RESPONSES[name]
        responses[error_data["status"]] = error_data["response"]

    return cast(dict[int | str, dict[str, Any]], responses)
