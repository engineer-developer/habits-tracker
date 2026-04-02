from aiogram import Bot
from dependency_injector.wiring import Provide, inject

from tg_bot import keyboards
from tg_bot.configs.loguru_config import logger
from tg_bot.containers.app_container import AppContainer
from tg_bot.schemas.habits import HabitByIdQuery, HabitJobCreateCommand
from tg_bot.services.api import ApiService


@inject
async def send_notify(
    cmd: HabitJobCreateCommand,
    api_service: ApiService = Provide[AppContainer.api_service],
    bot: Bot = Provide[AppContainer.telegram_bot],
) -> None:
    """Отправляем напоминание о привычке в чат пользователю."""
    habit = await api_service.get_habit_by_id(
        query=HabitByIdQuery(id=cmd.habit_id),
    )
    if habit is None:
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
        reply_markup=keyboards.kb_confirm_habit_completed(habit_id=habit.id),
    )
