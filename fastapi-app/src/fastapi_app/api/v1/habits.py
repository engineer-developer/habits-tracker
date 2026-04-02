"""Модуль представлений привычек."""

from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import Path, Query, status, Depends
from fastapi.routing import APIRouter
from pydantic import PositiveInt
from fastapi.responses import JSONResponse

from fastapi_app.dependencies.auth import (
    DepsCurrentUserTelegramId,
    get_current_user_telegram_id,
)
from fastapi_app.dependencies.habit import DepsHabitService
from fastapi_app.dependencies.users import DepsUserService
from fastapi_app.schemas.habits import (
    HabitByIdQuery,
    HabitByUserIdQuery,
    HabitCreateCommand,
    HabitDeleteCommand,
    HabitRead,
    HabitUpdateCommand,
    DeletedHabitsIds,
)
from fastapi_app.schemas.users import UserByTelegramIdQuery

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=HabitRead,
)
@inject
async def create_habit(
    telegram_id: DepsCurrentUserTelegramId,
    user_service: DepsUserService,
    habit_service: DepsHabitService,
    cmd: HabitCreateCommand,
) -> HabitRead:
    """Роут для создания привычки."""
    user = await user_service.get_user_by_telegram_id(
        query=UserByTelegramIdQuery(telegram_id=telegram_id)
    )
    cmd.user_id = user.id
    habit = await habit_service.add_habit(cmd)
    return habit


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description="""Роут для получения привычек пользователя.

    По умолчанию отдает все невыполненные привычки.
    Выполненные привычки отдает если передать query параметр completed=True.
    """,
    response_model=list[HabitRead],
)
@inject
async def get_all_habits_of_user(
    telegram_id: DepsCurrentUserTelegramId,
    user_service: DepsUserService,
    habit_service: DepsHabitService,
    completed: bool = Query(
        default=False, description="Фильтр привычек по состоянию выполнения."
    ),
) -> list[HabitRead]:
    """Роут для получения привычек пользователя."""
    user = await user_service.get_user_by_telegram_id(
        query=UserByTelegramIdQuery(telegram_id=telegram_id)
    )
    habits = await habit_service.get_all_habits_by_user_id(
        query=HabitByUserIdQuery(user_id=user.id),
        completed=completed,
    )
    return habits


@router.get(
    "/{id:int}",
    status_code=status.HTTP_200_OK,
    response_model=HabitRead,
)
@inject
async def get_habit_by_id(
    query: Annotated[HabitByIdQuery, Path()],
    habit_service: DepsHabitService,
) -> HabitRead:
    """Роут получения привычки по id."""
    habit = await habit_service.get_habit_by_id(query)
    return habit


@router.patch(
    "/{id}",
    response_model=HabitRead,
)
@inject
async def update_habit(
    cmd: HabitUpdateCommand,
    habit_service: DepsHabitService,
    id: int = Path(..., ge=1, description="ID привычки", examples=[1]),
) -> HabitRead:
    """Роут для изменения привычки."""
    habit = await habit_service.update_habit(habit_id=id, cmd=cmd)
    return habit


@router.delete(
    "/{id:int}",
    status_code=status.HTTP_200_OK,
    response_model=HabitRead,
    dependencies=[Depends(get_current_user_telegram_id)],
)
@inject
async def delete_habit(
    id: Annotated[int, Path(ge=1, description="ID привычки")],
    habit_service: DepsHabitService,
) -> HabitRead:
    """Роут для удаления привычки."""
    habit = await habit_service.delete_habit(habit_id=id)
    return habit


@router.delete(
    "/completed",
    status_code=status.HTTP_200_OK,
    response_model=DeletedHabitsIds,
)
@inject
async def delete_completed_habits(
    telegram_id: DepsCurrentUserTelegramId,
    habit_service: DepsHabitService,
) -> DeletedHabitsIds:
    """Роут для удаления завершенных привычек."""
    return await habit_service.delete_completed_habits_by_user_telegram_id(
        query=UserByTelegramIdQuery(telegram_id=telegram_id)
    )
