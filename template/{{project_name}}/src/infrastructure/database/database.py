from typing import Union
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.infrastructure.database.seed.app_data_seed import AppDataSeed


class Database:

    instance: Union["Database", None] = None

    @classmethod
    def set(cls, database: "Database"):
        if cls.instance is None:
            cls.instance = database

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False)
        Database.set(self)

    async def create_tables(self):
        from src.infrastructure.database import models

        async with self.engine.begin() as conn:
            print("Creating tables...")
            await conn.run_sync(SQLModel.metadata.create_all)

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            print("Dropping tables...")
            await conn.run_sync(SQLModel.metadata.drop_all)

    async def seed(self):
        gen = get_db_session()
        session = await anext(gen)
        app_data_seed = AppDataSeed(session)
        await app_data_seed.seed()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db = Database.instance
    if db is None:
        raise Exception("Database instance is not set.")
    async_session = async_sessionmaker(
        bind=db.engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session