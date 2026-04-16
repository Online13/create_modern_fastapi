from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.presentation.error import error_handler
from src.modules import base_routes
from src.modules.doc import doc_routes
from src.modules.doc.domain import doc_constants


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(api: FastAPI):
        print("Starting up application...")
        yield
        print("Shutting down application...")

    api = FastAPI(
        version=doc_constants.DOC_VERSION,
        title=doc_constants.DOC_TITLE,
        lifespan=lifespan,
        responses=error_handler.create_error_response("InvalidData"),
        **doc_constants.secure_doc_options,
    )

    error_handler.bind(api)

    api.include_router(base_routes.router, prefix="/api")
    api.include_router(doc_routes.router, prefix="/api")

    return api
