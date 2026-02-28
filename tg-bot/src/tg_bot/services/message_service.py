"""Модуль отправки сообщений."""

from dataclasses import dataclass

import loguru
from pydantic import ValidationError
from telebot import TeleBot

from configs.bot_factory import bot
from keyboards.kb_factory import kb_confirm_habit_completed
from schemas.habits import HabitDataDto
from services.logging_service import logger
from services.redis_service import RedisService, redis_service
from services.request_service import requests_service, NoAuthSessionStrategy
from services.scheduler_service import scheduler_service


def calculate_left_remind_quantity(habit_info: dict) -> int | bool:
    """Считаем количество оставшихся напоминаний."""
    reminder: dict = habit_info.get("reminder")
    if reminder is None:
        logger.error("Нет напоминаний.")
        return False

    planned_remind_quantity = reminder.get("remind_quantity")
    if planned_remind_quantity is None:
        logger.error("Нет количества напоминаний.")
        return False

    tracking: list = habit_info.get("tracking")
    if tracking is None:
        logger.error("Нет отслеживаний напоминаний.")
        return False

    completed_reminders = len(tracking)
    diff = planned_remind_quantity - completed_reminders
    logger.debug("Оставшееся количество напоминаний: {}", diff)
    return diff


def send_notice(**kwargs) -> bool:
    """Отправляем напоминание о привычке в чат пользователю."""
    try:
        habit_job_data = HabitDataDto(**kwargs)
        logger.debug("Данные из job: {}", habit_job_data.model_dump())
    except ValidationError as exc:
        logger.error(exc.errors())
        return False

    user_id = habit_job_data.user_id
    habit_name = habit_job_data.name
    job_id = habit_job_data.job_id

    requests_service.strategy = NoAuthSessionStrategy()
    habit_info: dict = requests_service.get_habit_info(
        job_id=job_id,
        name=habit_name,
    )
    if not habit_info:
        logger.error("Данные о привычке не получены из бэкэнда.")
        return False

    left_remind_quantity = calculate_left_remind_quantity(habit_info)
    if left_remind_quantity and left_remind_quantity > 0:
        msg_text = (
            f"Напоминание о привычке: *{habit_name}*\n"
            f"Описание: *{habit_job_data.description}*\n"
            f"Время выполнения: *{habit_job_data.remind_time}*\n"
            f"Осталось выполнить: *{left_remind_quantity}*"
        )
        bot.send_message(
            chat_id=habit_job_data.chat_id,
            text=msg_text,
            reply_markup=kb_confirm_habit_completed(habit_name=habit_name),
            parse_mode="Markdown",
        )
    else:
        scheduler_service.scheduler.remove_job(job_id=job_id)
        logger.debug("Задача c job_id={} удалена.", job_id)
    return True


@dataclass
class TgBotMessageService:
    """Сервис отправки сообщений ботом."""

    bot: TeleBot
    logger: loguru.logger
    redis_service: RedisService


bot_message_service = TgBotMessageService(
    bot=bot,
    logger=logger,
    redis_service=redis_service,
)
