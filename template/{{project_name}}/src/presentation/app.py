from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.domain.entities.doc import DOC_TITLE, DOC_VERSION
from src.infrastructure.database.interface import Database
from src.presentation.core.error_handler import create_error_response, handle_error
from src.presentation.routes import app_routes


class App:

    database: Database

    def __init__(self, database: Database):
        self.database = database
        self.api = FastAPI(
            version=DOC_VERSION,
            title=DOC_TITLE,
            lifespan=self.lifespan,
            responses=create_error_response("InvalidData"),
        )

    @asynccontextmanager
    async def lifespan(self, api: FastAPI):
        print("Starting up application...")
        await self.database.create_tables()
        await self.database.seed()
        yield
        print("Shutting down application...")
        await self.database.drop_tables()

    def setup_api(self):
        handle_error(self.api)

        self.api.include_router(app_routes.router, prefix="/api/v1")
