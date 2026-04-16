from sqlalchemy.ext.asyncio import AsyncEngine
from src.infrastructure.env.interface import Settings

class Container:
    
    database_engine: AsyncEngine

    @classmethod
    def get_database_engine(cls) -> AsyncEngine:
        if not hasattr(cls, "database_engine"):
            raise Exception("Database engine is not initialized.")
        return cls.database_engine
    
    @classmethod
    def get_settings(cls) -> Settings:
        if not hasattr(cls, "settings"):
            raise Exception("Settings is not initialized.")
        return cls.settings
    
    settings: Settings

    @classmethod
    def set_settings(cls, settings: Settings):
        cls.settings = settings

    @classmethod
    def set_database_engine(cls, engine: AsyncEngine):
        cls.database_engine = engine
