"""Модуль представлений привычек."""

from typing import Annotated

from core.database import CommonAsyncSession
from core.loguru_config import logger
from fastapi import HTTPException
from fastapi.params import Path
from fastapi.routing import APIRouter
from models.app_models import Habit, Reminder, Tracking
from schemas.habit_schema import (
    HabitAddDto,
    HabitCompletedDto,
    HabitDeleteInfoDto,
    HabitOutDto,
    HabitPatchDto,
)
from services.habit_service import (
    delete_habit_by_name_and_user_id,
    fetch_all_habit_by_user_id,
    fetch_habit_by_name_and_job_id,
    fetch_habit_by_name_and_user_id,
)
from sqlalchemy.exc import IntegrityError

from api.auth.dependencies import GetCurrentActiveUser

router = APIRouter(prefix="/habits", tags=["habits"])


@router.get(
    "/",
    description="Получение всех привычек пользователя.",
    response_model=list[HabitOutDto],
)
async def get_all_users_habits(
    user: GetCurrentActiveUser,
    session: CommonAsyncSession,
) -> list[HabitOutDto]:
    """Представление для получения всех привычек пользователя."""
    habits_orm = await fetch_all_habit_by_user_id(user_id=user.id, session=session)

    if not habits_orm:
        logger.error("Привычек не найдено.")
        raise HTTPException(status_code=404, detail="Привычек не найдено.")

    habits_dto = [HabitOutDto.model_validate(habit) for habit in habits_orm]
    return habits_dto


@router.post(
    "/",
    description="Добавление новой привычки",
    response_model=HabitOutDto,
)
async def add_habit(
    habit_data: HabitAddDto,
    user: GetCurrentActiveUser,
    session: CommonAsyncSession,
) -> HabitOutDto:
    """Представление для добавления привычки."""
    reminder = Reminder(
        remind_time=habit_data.remind_time,
        remind_quantity=habit_data.remind_quantity,
        job_id=habit_data.job_id,
    )

    habit = await fetch_habit_by_name_and_user_id(name=habit_data.name, user_id=user.id, session=session)

    if habit is None:
        habit = Habit(
            name=habit_data.name,
            description=habit_data.description,
        )
        habit.reminder = reminder
        user.habits.append(habit)
        # session.add_all([habit, reminder])

    elif habit and habit.completed:
        habit.completed = False
        habit.description = habit_data.description
        habit.reminder

    elif habit and not habit.completed:
        error_msg = "Привычка с таким названием уже контролируется."
        logger.error(error_msg)
        raise HTTPException(
            status_code=409,
            detail=error_msg,
        )

    await session.commit()

    # try:
    #     await session.commit()
    # except IntegrityError as exc:
    #     error_msg = f"Привычка с такими данными уже есть: {exc.orig}"
    #     logger.error(error_msg)
    #     raise HTTPException(
    #         status_code=409,
    #         detail=error_msg,
    #     )
    await session.refresh(habit, ["user", "reminder", "tracking"])

    logger.debug("Добавлена привычка '{}'.", habit)
    return HabitOutDto.model_validate(habit)


@router.get(
    "/{name:str}/reminders/{job_id:str}/",
    description="Получение привычки по названию и id задачи",
    response_model=HabitOutDto,
)
async def get_habit_by_name_and_job_id(
    name: Annotated[str, Path()],
    job_id: Annotated[str, Path()],
    session: CommonAsyncSession,
) -> HabitOutDto:
    """Представление для получения привычки по названию и id задачи."""
    habit = await fetch_habit_by_name_and_job_id(
        name=name,
        job_id=job_id,
        session=session,
    )
    if not habit:
        logger.error("Привычки '{}' не найдено.", name)
        raise HTTPException(status_code=404, detail=f"Привычки '{name}' не найдено.")

    return HabitOutDto.model_validate(habit)


@router.get(
    "/{name:str}/",
    description="Получение привычки по названию.",
    response_model=HabitOutDto,
)
async def get_habit_by_name(
    name: Annotated[str, Path()],
    user: GetCurrentActiveUser,
    session: CommonAsyncSession,
) -> HabitOutDto:
    """Представление для получения привычки по названию."""
    habit = await fetch_habit_by_name_and_user_id(
        name=name,
        user_id=user.id,
        session=session,
    )
    if not habit:
        logger.error("Привычки '{}' не найдено.", name)
        raise HTTPException(status_code=404, detail=f"Привычки '{name}' не найдено.")

    return HabitOutDto.model_validate(habit)


@router.patch(
    "/{name:str}/",
    description="Изменение привычки",
    response_model=HabitOutDto,
)
async def patch_habit(
    name: Annotated[str, Path()],
    habit_data: HabitPatchDto,
    user: GetCurrentActiveUser,
    session: CommonAsyncSession,
) -> HabitOutDto:
    """Представление для изменения привычки."""
    habit = await fetch_habit_by_name_and_user_id(
        name=name,
        user_id=user.id,
        session=session,
    )
    if not habit:
        logger.error("Привычки '{}' не найдено.", habit_data.name)
        raise HTTPException(
            status_code=404, detail=f"Привычки '{habit_data.name}' не найдено."
        )

    if habit_data.name:
        habit.name = habit_data.name

    if habit_data.description:
        habit.description = habit_data.description

    if habit_data.remind_quantity and habit_data.remind_quantity > 0:
        habit.reminder.remind_quantity = habit_data.remind_quantity

    if habit_data.remind_time:
        habit.reminder.remind_time = habit_data.remind_time

    await session.commit()
    await session.refresh(habit, ["reminder", "tracking"])

    logger.debug("Изменена привычка '{}'.", habit)
    return HabitOutDto.model_validate(habit)


@router.delete(
    "/{name:str}/",
    description="Удаление привычки",
    response_model=HabitDeleteInfoDto,
)
async def delete_habit(
    name: Annotated[str, Path()],
    user: GetCurrentActiveUser,
    session: CommonAsyncSession,
) -> HabitDeleteInfoDto:
    """Представление для удаления привычки."""
    if not name:
        logger.error("Не указано название привычки.")
        raise HTTPException(status_code=400, detail="Не указано название привычки.")

    deleted_habit_id = await delete_habit_by_name_and_user_id(
        name=name,
        user_id=user.id,
        session=session,
    )
    if not deleted_habit_id:
        logger.error("Привычки '{}' не найдено.", name)
        raise HTTPException(status_code=404, detail=f"Привычки '{name}' не найдено.")
    return HabitDeleteInfoDto(habit_id=deleted_habit_id)


@router.post(
    "/confirm_completed/",
    description="Регистрация выполнения привычки",
    response_model=HabitOutDto,
)
async def process_mark_completion(
    confirm_data: HabitCompletedDto,
    user: GetCurrentActiveUser,
    session: CommonAsyncSession,
) -> HabitOutDto:
    """Представление для регистрации выполнения привычки."""
    habit = await fetch_habit_by_name_and_user_id(
        name=confirm_data.name,
        user_id=user.id,
        session=session,
    )
    if not habit:
        logger.error("Привычки '{}' не найдено.", confirm_data.name)
        raise HTTPException(
            status_code=404,
            detail=f"Привычки '{confirm_data.name}' не найдено.",
        )

    tracking_orm = Tracking(alert_time=confirm_data.alert_time)
    habit.tracking.append(tracking_orm)
    await session.commit()
    await session.refresh(habit, ["reminder", "tracking"])
    logger.debug("Зарегистрировано выполнение привычки '{}'.", habit)

    if habit.reminder.remind_quantity == len(habit.tracking):
        habit.completed = True
        logger.debug("Привитие привычки '{}' завершено.", habit)
        await session.commit()
        # await session.refresh(habit, ["reminder", "tracking"])

    return HabitOutDto.model_validate(habit)
