from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.container import Container
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


def setup_database(database_url: str):
    """
    Setup the database connection and initialize the engine.
    """
    engine = create_async_engine(database_url)
    Container.set_database_engine(engine)


async def create_tables():
    """
    Create tables in the database based on the defined SQLModel models.
    """
    engine = Container.get_database_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_tables():
    """
    Drop tables in the database based on the defined SQLModel models.
    """
    engine = Container.get_database_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def seed_database(database_type: str, verbose: bool = True):
    """
    Seed the database with initial data based on the specified database type.
    """
    # Execute the seeding logic
    raise NotImplementedError("Seeding logic is not implemented yet.")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session for use in the application.
    """
    engine = Container.get_database_engine()
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
