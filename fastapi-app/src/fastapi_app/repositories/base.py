from abc import ABC
from models import Model as OrmModel
from typing import TypeVar

__all__ = (
    "Repository",
    "BaseRepository",
)


BaseRepository = TypeVar("BaseRepository", bound="Repository")


class Repository(ABC):
    async def create(self, cmd: OrmModel) -> OrmModel:
        """Create OrmModel."""
        raise NotImplemented

    async def read(self, query: int) -> OrmModel:
        """Read OrmModel."""
        raise NotImplemented

    async def read_all(self) -> list[OrmModel]:
        """Read all OrmModels."""
        raise NotImplemented

    async def update(self, cmd: OrmModel) -> OrmModel:
        """Update OrmModel."""
        raise NotImplemented

    async def delete(self, cmd: OrmModel) -> OrmModel:
        """Delete OrmModel."""
        raise NotImplemented
