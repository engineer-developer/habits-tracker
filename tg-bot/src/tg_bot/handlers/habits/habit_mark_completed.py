from datetime import datetime

from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from tg_bot.callbacks.habits import HabitMarkCompletedCallback, HabitMarkCompletedAction
from tg_bot.configs.loguru_config import logger
from tg_bot.handlers.main_menu import show_message_with_register_or_login, show_user_profile
from tg_bot.services.api import ApiService
from tg_bot.services.redis import RedisService
from tg_bot.services.scheduler import SchedulerService
from tg_bot.schemas.habits import HabitByIdQuery
from tg_bot.schemas.tracking import TrackingCreateCommand


router = Router(name="habit_mark_completed")


@router.callback_query(
    HabitMarkCompletedCallback.filter(
        F.action == HabitMarkCompletedAction.mark_completed
    ),
)
async def habit_mark_completed(
    callback: CallbackQuery,
    state: FSMContext,
    api_service: ApiService,
    redis_service: RedisService,
    scheduler_service: SchedulerService,
):
    """Фиксирует факт выполнения привычки после напоминания."""
    habit_id = int(callback.data.split(sep=":")[-1])
    token = await redis_service.get_token(telegram_id=callback.from_user.id)
    if not token:
        logger.error("Нет токена доступа.")
        await show_message_with_register_or_login(message=callback.message)
        return

    tracking = await api_service.add_tracking_of_habit(
        token,
        TrackingCreateCommand(
            habit_id=habit_id,
            execution_time=datetime.now(),
        ),
    )
    if not tracking:
        logger.error("Ошибка добавления отслеживания.")
        return

    logger.debug(f"Выполнение привычки с id={habit_id} зафиксировано.")

    habit = await api_service.get_habit_by_id(query=HabitByIdQuery(id=habit_id))
    if not habit:
        logger.error("Не удалось получить данные привычки")

    if not habit.completed:
        await callback.message.answer("Выполнение привычки зафиксировано 👍.")
        await show_user_profile(message=callback.message)

    if habit.completed:
        result = await scheduler_service.delete_job(job_id=str(habit.id))
        if not result:
            logger.error(f"Не удалось отключить напоминания для привычки id={habit.id}")
            return
        logger.debug(f"Напоминания для привычки id={habit.id} отключены.")
        await callback.message.answer(f"Привитие привычки '{habit.title}' завершено 🏆.")
        await show_user_profile(message=callback.message)