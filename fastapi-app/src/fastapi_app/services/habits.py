"""Модуль обслуживания привычек."""

from sqlalchemy.exc import DatabaseError

from fastapi_app.configs.loguru_config import logger
from fastapi_app.exceptions.repositories import EmptyResult
from fastapi_app.exceptions.services import (
    DbException,
    HabitNotFoundException,
)
from fastapi_app.repositories.habits import HabitRepository
from fastapi_app.schemas.habits import (
    HabitByIdQuery,
    HabitByUserIdQuery,
    HabitCreateCommand,
    HabitDeleteCommand,
    HabitRead,
    HabitUpdateCommand,
)


class HabitService:
    """Сервис привычек."""

    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    async def add_habit(self, cmd: HabitCreateCommand) -> HabitRead:
        """Добавляет привычку."""
        try:
            habit = await self.repository.create(cmd)
        except DatabaseError as exc:
            raise DbException(message=repr(exc))
        return habit

    async def get_habit_by_id(self, query: HabitByIdQuery) -> HabitRead:
        """Получает привычку по id."""
        try:
            habit = await self.repository.read(query)
        except EmptyResult:
            raise HabitNotFoundException
        return habit

    async def get_all_habits_by_user_id(
        self,
        query: HabitByUserIdQuery,
        completed: bool,
    ) -> list[HabitRead]:
        """Получает все привычки пользователя."""
        try:
            habit = await self.repository.read_all_by_user_id(query, completed)
        except EmptyResult:
            raise HabitNotFoundException
        return habit

    async def update_habit(self, cmd: HabitUpdateCommand) -> HabitRead:
        """Обновляет данные привычки."""
        try:
            habit = await self.repository.update(cmd)
        except EmptyResult:
            raise HabitNotFoundException
        return habit

    async def delete_habit(self, cmd: HabitDeleteCommand) -> HabitRead:
        """Удаляет привычку."""
        try:
            habit = await self.repository.delete(cmd)
        except EmptyResult:
            raise HabitNotFoundException
        return habit

    async def mark_habit_as_completed(self, query: HabitByIdQuery) -> None:
        """Отмечает привычку как выполненная если выполнено условие того,
        что количество отслеживаний равно количеству необходимых напоминаний.
        """
        habit = await self.repository.read(query)
        if len(habit.tracking) >= habit.remind_quantity:
            cmd = HabitUpdateCommand(id=habit.id, completed=True)
            habit = await self.repository.update(cmd=cmd)

        if habit.completed:
            logger.debug("Привитие привычки '{}' завершено.", habit.title)
