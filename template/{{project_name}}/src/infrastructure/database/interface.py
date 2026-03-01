
from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncEngine


class Database(Protocol):

    engine: AsyncEngine
    
    async def create_tables(self):
        ...

    async def drop_tables(self):
        ...

    async def seed(self):
        ...