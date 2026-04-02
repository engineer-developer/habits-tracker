from datetime import datetime

from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.scene import ScenesManager
from aiogram.types import CallbackQuery

from tg_bot import callbacks, schemas, services
from tg_bot import scenes as app_scenes
from tg_bot.configs.loguru_config import logger

router = Router(name="habit_mark_completed")


@router.callback_query(
    callbacks.HabitMarkCompletedCallback.filter(
        F.action == callbacks.HabitMarkCompletedAction.mark_completed
    ),
)
async def habit_mark_completed(
    callback_query: CallbackQuery,
    scenes: ScenesManager,
    api_service: services.ApiService,
    redis_service: services.RedisService,
    scheduler_service: services.SchedulerService,
) -> None:
    """Фиксирует факт выполнения привычки после напоминания."""
    habit_id = int(callback_query.data.split(sep=":")[-1])
    token = await redis_service.get_token(telegram_id=callback_query.from_user.id)
    if token is None:
        return await scenes.enter(app_scenes.MainMenuScene)

    tracking = await api_service.add_tracking_of_habit(
        token,
        schemas.TrackingCreateCommand(
            habit_id=habit_id,
            execution_time=datetime.now(),
        ),
    )
    if tracking is None:
        logger.error("Ошибка добавления отслеживания.")
        return await scenes.enter(app_scenes.MainMenuScene)

    logger.debug(f"Выполнение привычки с id={habit_id} зафиксировано.")

    habit = await api_service.get_habit_by_id(query=schemas.HabitByIdQuery(id=habit_id))
    if habit is None:
        logger.error("Не удалось получить данные привычки")
        return await scenes.enter(app_scenes.MainMenuScene)

    if habit.completed:
        result = await scheduler_service.delete_job(job_id=str(habit.id))
        if not result:
            logger.error(f"Не удалось отключить напоминания для привычки id={habit.id}")
            return

        logger.debug(f"Напоминания для привычки id={habit.id} отключены.")
        await callback_query.message.answer(
            f"Привитие привычки '{habit.title}' завершено 🏆🏆🏆"
        )
    else:
        await callback_query.message.answer("Выполнение привычки зафиксировано 👍")

    await scenes.enter(app_scenes.MainMenuScene)
