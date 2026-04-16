from dataclasses import dataclass
from typing import TypeVar, Generic

from pydantic import BaseModel

Data = TypeVar("Data")


@dataclass(frozen=True)
class Response(BaseModel, Generic[Data]):
    success: bool
    message: str
    data: Data


class PaginationMetadata(BaseModel):
    total: int
    limit: int
    offset: int


class PaginatedResponse(BaseModel, Generic[Data]):
    success: bool
    message: str
    data: Data
    meta: PaginationMetadata

