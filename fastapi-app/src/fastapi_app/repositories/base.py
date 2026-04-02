from abc import ABC
from typing import TypeVar

from fastapi_app.schemas.base import Model

__all__ = (
    "Repository",
    "BaseRepository",
)


BaseRepository = TypeVar("BaseRepository", bound="Repository")


class Repository(ABC):
    """Базовый репозиторий."""

    async def create(self, cmd: Model) -> Model:
        """Create Model."""
        raise NotImplementedError

    async def read(self, query: Model) -> Model:
        """Read Model."""
        raise NotImplementedError

    async def read_all(self) -> list[Model]:
        """Read all Models."""
        raise NotImplementedError

    async def update(self, id: int, cmd: Model) -> Model:
        """Update Model."""
        raise NotImplementedError

    async def delete(self, id: int) -> Model:
        """Delete Model."""
        raise NotImplementedError
