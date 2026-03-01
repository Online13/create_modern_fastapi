from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings
from src.infrastructure.database.models.app_models import AppData


class AppDataSeed:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def seed(self):
        result = await self.session.exec(
            select(AppData).where(AppData.version == settings.api_version)
        )
        app_data = result.first()
        if app_data is None:
            app_data = AppData(id=1, name="My App", version=settings.api_version)
            self.session.add(app_data)
            await self.session.commit()

    async def clear(self):
        result = await self.session.exec(
            select(AppData).where(AppData.version == settings.api_version)
        )
        app_data = result.first()
        if app_data is not None:
            await self.session.delete(app_data)
        await self.session.commit()
