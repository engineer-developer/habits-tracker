from aiogram import Bot
from tg_bot.configs.loguru_config import logger
from tg_bot.containers.app_container import AppContainer
from tg_bot.keyboards.kb_factory import kb_confirm_habit_completed
from tg_bot.services.scheduler import SchedulerService
from tg_bot.schemas.habits import HabitJobCreateCommand, HabitByIdQuery
from tg_bot import main
from tg_bot.services.api import ApiService


async def send_notify(cmd: HabitJobCreateCommand, **kwargs) -> None:
    """Отправляем напоминание о привычке в чат пользователю."""
    container: AppContainer = main.app_context.get("container")
    api_service: ApiService = await container.api_service()
    scheduler_service: SchedulerService = await container.scheduler_service()
    bot: Bot = await container.telegram_bot()

    habit = await api_service.get_habit_by_id(
        query=HabitByIdQuery(id=cmd.habit_id),
    )
    if not habit:
        logger.error(f"Не удалось получить данные привычки c id={cmd.habit_id}")
        return

    left_remind_quantity = habit.remind_quantity - len(habit.tracking)
    msg_text = (
        f"Напоминание о привычке: {habit.title}\n"
        f"Описание: {habit.description}\n"
        f"Время выполнения: {habit.remind_time}\n"
        f"Осталось выполнить: {left_remind_quantity} раз(а)"
    )
    await bot.send_message(
        chat_id=cmd.user_id,
        text=msg_text,
        reply_markup=kb_confirm_habit_completed(habit_id=habit.id),
    )
