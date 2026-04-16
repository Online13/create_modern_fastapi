from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime, func

class TimestampedModel(SQLModel):
    created_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={
            "server_default": func.now(),
            "nullable": True,
        },
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
            "nullable": False,
        },
    )


class BaseSQLModel(TimestampedModel):
    id: int | None = Field(primary_key=True, index=True, default=None)