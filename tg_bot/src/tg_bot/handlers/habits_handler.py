"""Модуль обработки сообщений и callbacks о привычках."""

import datetime
import uuid

from pydantic import ValidationError
from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from tg_bot.core.config import Settings
from tg_bot.keyboards import kb_factory
from tg_bot.keyboards.kb_factory import kb_habit_add_or_cancel, kb_habits_list
from tg_bot.schemas.habit_schema import HabitDataDto
from tg_bot.service_layer.logging_service import logger
from tg_bot.service_layer.message_service import send_notice
from tg_bot.service_layer.notify_service import HabitNotifyService, habit_notify_service
from tg_bot.service_layer.redis_service import redis_service
from tg_bot.service_layer.request_service import requests_service, TokenAuthSessionStrategy
from tg_bot.service_layer.scheduler_service import scheduler_service
from tg_bot.states.states import HabitAddStates


def register_handlers(bot: TeleBot, settings: Settings) -> None:
    """Регистрируем обработчики команд."""

    @bot.callback_query_handler(
        func=lambda callback: callback.data == "menu_habits_list"
    )
    def get_all_habits(callback: CallbackQuery) -> None:
        """Обработчик callback для получения всех привычек пользователя."""
        token = redis_service.load_user_data(user_id=callback.from_user.id, key="token")
        requests_service.strategy = TokenAuthSessionStrategy(token=token)
        habits_info: list[dict] = requests_service.get_all_habits_info()
        if habits_info:
            bot.send_message(
                chat_id=callback.message.chat.id,
                text="Вырабатываем привычки:",
                reply_markup=kb_habits_list(habits_info),
            )
        else:
            bot.send_message(
                chat_id=callback.message.chat.id,
                text="Пока нет привычек для привития.",
            )

    @bot.callback_query_handler(func=lambda callback: callback.data == "menu_add_habit")
    def add_habit(callback: CallbackQuery) -> None:
        """Обработчик callback добавления привычки."""

        msg = bot.send_message(
            chat_id=callback.message.chat.id,
            text="Отправьте название привычки.",
        )
        bot.set_state(
            user_id=callback.from_user.id,
            state=HabitAddStates.wait_for_habit_name,
            chat_id=callback.message.chat.id,
        )
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
        )
        bot.register_next_step_handler(msg, get_habit_name)
        bot.answer_callback_query(callback.id)

    def get_habit_name(message: Message) -> None:
        """Получение названия привычки."""
        title = message.text
        logger.debug("Введено название привычки: {}", title)

        bot.add_data(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            title=title,
        )
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Добавьте описание привычки.",
        )

        bot.register_next_step_handler(msg, get_habit_description)

    def get_habit_description(message: Message) -> None:
        """Получение описания привычки."""
        description = message.text
        logger.debug("Введено описание: {}", description)

        bot.add_data(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            description=description,
        )
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Укажите время, в которое ежедневно будут приходить напоминания.\n"
            "Например - 10:45",
        )
        bot.register_next_step_handler(msg, get_habit_remind_time)

    def get_habit_remind_time(message: Message) -> None:
        """Получение времени напоминания."""
        remind_time = message.text
        try:
            remind_time = datetime.time.fromisoformat(remind_time)
            logger.debug("Введено время: {}", remind_time)

        except ValueError as exc:
            logger.error("Не верно указано время: {}", exc)
            msg = bot.send_message(
                chat_id=message.chat.id,
                text="Не верно указано время. Укажите в формате: ЧЧ:ММ",
            )
            bot.register_next_step_handler(msg, get_habit_remind_time)
            return

        bot.add_data(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            remind_time=remind_time.strftime("%H:%M"),
        )
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Сколько раз нужно напомнить?",
        )
        bot.register_next_step_handler(msg, get_habit_remind_quantity)

    def get_habit_remind_quantity(message: Message) -> None:
        """Получение количества напоминаний."""
        remind_quantity = message.text
        try:
            remind_quantity = int(remind_quantity)
            logger.debug("Введено количество: {}", remind_quantity)
        except ValueError as exc:
            logger.error("Не верно указано количество: {}", exc)
            msg = bot.send_message(
                chat_id=message.chat.id,
                text="Не верно указано количество. Введите только цифры",
            )
            bot.register_next_step_handler(msg, get_habit_remind_quantity)
            return

        bot.add_data(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            remind_quantity=remind_quantity,
        )
        habit_data = {}
        with bot.retrieve_data(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        ) as data:
            logger.debug("Данные добавляемой привычки: {}", data)
            habit_data.update(data)

        text_parts = (
            f"Название привычки: *{habit_data.get('title')}*",
            f"Описание: *{habit_data.get('description')}*",
            f"Время напоминания: *{habit_data.get('remind_time')}*",
            f"Количество напоминаний: *{habit_data.get('remind_quantity')}*",
        )
        msg_text = "\n".join(text_parts)

        bot.send_message(
            chat_id=message.chat.id,
            text=msg_text,
            reply_markup=kb_habit_add_or_cancel(),
            parse_mode="Markdown",
        )

    @bot.callback_query_handler(func=lambda cb: cb.data == "cb_confirm_add_habit")
    def process_confirm_add_habit(callback: CallbackQuery) -> bool | None:
        """Обработка подтверждения добавления привычки.

        - Направление информации о привычке в бэкэнд.
        - Добавление задания о напоминании в APScheduler.
        """
        habit_data = dict()
        with bot.retrieve_data(
            user_id=callback.from_user.id,
            chat_id=callback.message.chat.id,
        ) as data:
            habit_data.update(data)

        habit_data["user_id"] = callback.from_user.id
        habit_data["chat_id"] = callback.message.chat.id

        success = habit_notify_service.process_notify(
            func=send_notice,
            habit_data=habit_data,
        )
        if not success:
            logger.error("Не удалось обработать данные.")
            bot.answer_callback_query(
                callback_query_id=callback.id,
                text="Возможно такая привычка уже есть.",
            )
            return False

        bot.delete_state(
            user_id=callback.from_user.id,
            chat_id=callback.message.chat.id,
        )
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
        )
        logger.debug("Привычка добавлена.")
        bot.answer_callback_query(callback.id, "Привычка добавлена.")

    @bot.callback_query_handler(func=lambda cb: cb.data == "cb_cancel_add_habit")
    def process_cancel_add_habit(callback: CallbackQuery) -> None:
        """Отмена добавления привычки."""
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="🏠 Добро пожаловать в личный кабинет",
            reply_markup=kb_factory.kb_profile(),
        )
        bot.delete_state(
            user_id=callback.from_user.id,
            chat_id=callback.message.chat.id,
        )
        logger.debug("Добавление привычки отменено.")
        bot.answer_callback_query(callback.id, "Добавление отменено")

    @bot.callback_query_handler(
        func=lambda cb: cb.data.startswith("cb_confirm_habit_done")
    )
    def process_confirm_habit_completed(callback: CallbackQuery) -> None:
        """Подтверждение выполнения привычки."""
        habit_name = callback.data.split(":")[1]

        confirm_datetime = datetime.datetime.now(tz=datetime.UTC)
        confirm_data = {
            "name": habit_name,
            "alert_time": confirm_datetime.isoformat(),
        }
        token = redis_service.load_user_data(callback.from_user.id, "token")
        requests_service.strategy = TokenAuthSessionStrategy(token=token)

        success = requests_service.upload_habit_confirm_data(data=confirm_data)

        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
        )
        if not success:
            bot.answer_callback_query(
                callback.id,
                text="Не удалось зафиксировать выполнение привычки.",
            )
            return
        bot.answer_callback_query(callback.id)
        msg_text = f"Выполнение привычки '{habit_name}' зафиксировано 👍"
        bot.send_message(
            chat_id=callback.message.chat.id,
            text=msg_text,
        )
