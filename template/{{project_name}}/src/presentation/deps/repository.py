from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.infrastructure.database.dependencies import get_db_session

# Database
# -----------------------------------------------------------------------------

DatabaseDep = Annotated[AsyncSession, Depends(get_db_session)]


# Repositories
# -----------------------------------------------------------------------------
