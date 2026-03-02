"""Модуль операций с пользователями."""

from sqlalchemy.exc import DatabaseError

from fastapi_app.exceptions.repositories import EmptyResult, EntityAlreadyExist
from fastapi_app.exceptions.services import (
    DbException,
    UserAlreadyExistException,
    UserIsNotActiveException,
    UserNotFoundException,
)
from fastapi_app.repositories.users import UserRepository
from fastapi_app.schemas.users import (
    UserByTelegramIdQuery,
    UserCreateCommand,
    UserRead,
    UserReadWithPassword,
)


class UserService:
    """Сервис пользователей."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def add_user(self, cmd: UserCreateCommand) -> UserRead:
        """Добавляем пользователя в БД."""
        try:
            user = await self.repository.create(cmd)
        except EntityAlreadyExist:
            raise UserAlreadyExistException
        except DatabaseError as exc:
            raise DbException(message=repr(exc))
        return user

    async def get_all_users(self) -> list[UserRead]:
        """Получаем всех пользователей из БД."""
        return await self.repository.read_all()

    async def get_all_active_users(self) -> list[UserRead]:
        """Получаем всех активных пользователей из БД."""
        users = await self.get_all_users()
        return [user for user in users if user.is_active]

    async def get_user_by_telegram_id(
        self,
        query: UserByTelegramIdQuery,
    ) -> UserReadWithPassword:
        """Получаем пользователя по его telegram_id."""
        try:
            user = await self.repository.read_by_telegram_id(query)
        except EmptyResult:
            raise UserNotFoundException
        return user

    async def get_current_active_user_with_password(
        self, query: UserByTelegramIdQuery
    ) -> UserReadWithPassword:
        """Получаем текущего активного пользователя с паролем."""
        user_dto = await self.get_user_by_telegram_id(query)
        if not user_dto.is_active:
            raise UserIsNotActiveException
        return user_dto

    async def get_current_active_user(
        self,
        query: UserByTelegramIdQuery,
    ) -> UserRead:
        """Получаем текущего активного пользователя без пароля."""
        user = await self.get_current_active_user_with_password(query)
        return UserRead(**user.model_dump())
