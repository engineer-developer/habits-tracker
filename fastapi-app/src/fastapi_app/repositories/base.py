from abc import ABC
from typing import TypeVar

from fastapi_app.models import Model as OrmModel

__all__ = (
    "Repository",
    "BaseRepository",
)


BaseRepository = TypeVar("BaseRepository", bound="Repository")


class Repository(ABC):
    """Базовый репозиторий."""

    async def create(self, cmd: OrmModel) -> OrmModel:
        """Create OrmModel."""
        raise NotImplementedError

    async def read(self, query: int) -> OrmModel:
        """Read OrmModel."""
        raise NotImplementedError

    async def read_all(self) -> list[OrmModel]:
        """Read all OrmModels."""
        raise NotImplementedError

    async def update(self, cmd: OrmModel) -> OrmModel:
        """Update OrmModel."""
        raise NotImplementedError

    async def delete(self, cmd: OrmModel) -> OrmModel:
        """Delete OrmModel."""
        raise NotImplementedError
