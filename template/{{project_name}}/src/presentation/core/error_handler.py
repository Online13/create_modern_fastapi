from typing import Any, Literal, TypedDict, cast
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.presentation.schemas.core import (
    ConflictErrorResponse,
    BadRequestErrorResponse,
    ErrorBaseResponse,
    ForbiddenErrorResponse,
    InternalServerErrorResponse,
    NotFoundErrorResponse,
    UnauthorizedErrorResponse,
    ValidationErrorResponse,
)


class AppException(HTTPException):
    def __init__(
        self, status_code: int, detail: str, code: str | None = None, **kwargs
    ):
        super().__init__(status_code=status_code, detail=detail, **kwargs)
        self.detail = detail
        self.code = code


def handle_error(app: FastAPI):
    @app.exception_handler(AppException)
    async def exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            # On récupère les headers s'ils existent dans l'exception
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
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):

        errors = {}
        for err in exc.errors():
            field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
            message = err["msg"]
            errors.setdefault(field, []).append(message)

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

