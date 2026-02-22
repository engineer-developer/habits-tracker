import models

from repositories.base import Repository


class HabitRepository(Repository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def create(self, cmd) -> models.Habit:
        pass

    async def read(self, query) -> models.Habit:
        pass

    async def read_all(self) -> list[models.Habit]:
        pass

    async def update(self, cmd) -> models.Habit:
        pass

    async def delete(self, cmd) -> models.Habit:
        pass
