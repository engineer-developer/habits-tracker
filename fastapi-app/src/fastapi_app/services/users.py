"""Модуль операций с пользователями."""

from models.users import User
from repositories.exceptions import EmptyResult, EntityAlreadyExist
from repositories.users import UserRepository
from schemas.users import UserCreateCommand, UserRead, UserReadWithPassword
from sqlalchemy.exc import DatabaseError

from services.exceptions import (
    DbException,
    UserAlreadyExistException,
    UserIsNotActiveException,
    UserNotFoundException,
)


class UserService:
    """Сервис пользователей."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def add_user(self, user: UserCreateCommand) -> UserRead:
        """Добавляем пользователя в БД."""
        try:
            user_orm = await self.repository.create(User(**user.model_dump()))
        except EntityAlreadyExist:
            raise UserAlreadyExistException()
        except DatabaseError as exc:
            raise DbException(detail=str(exc))
        return UserRead.model_validate(user_orm)

    async def get_all_users(self) -> list[UserRead]:
        """Получаем всех пользователей из БД."""
        users_orm = await self.repository.read_all()
        return [UserRead.model_validate(user) for user in users_orm if user]

    async def get_all_active_users(self) -> list[UserRead]:
        """Получаем всех активных пользователей из БД."""
        users = await self.get_all_users()
        return [user for user in users if user.is_active]

    async def get_user_by_telegram_id(self, telegram_id: int) -> User:
        """Получаем пользователя по его telegram_id."""
        try:
            user = await self.repository.read_by_telegram_id(telegram_id)
        except EmptyResult:
            raise UserNotFoundException()
        return user

    async def get_current_active_user_with_password(
        self, telegram_id: int
    ) -> UserReadWithPassword:
        """Получаем текущего активного пользователя."""
        user_orm = await self.get_user_by_telegram_id(telegram_id)
        if not user_orm.is_active:
            raise UserIsNotActiveException()
        user_dto = UserReadWithPassword.model_validate(user_orm)
        return user_dto

    async def get_current_active_user(self, telegram_id: int) -> UserRead:
        """Получаем текущего активного пользователя без пароля."""
        user = await self.get_current_active_user_with_password(telegram_id)
        return UserRead(**user.model_dump())
