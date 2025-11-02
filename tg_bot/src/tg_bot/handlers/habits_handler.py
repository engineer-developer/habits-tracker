"""Модуль обработки сообщений и callbacks о привычках."""

import datetime
import uuid

from pydantic import ValidationError
from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from tg_bot.core.config import Settings
from tg_bot.keyboards import kb_factory
from tg_bot.keyboards.kb_factory import kb_habit_add_or_cancel, kb_habits_list
from tg_bot.schemas.habit_schema import HabitData
from tg_bot.services.logging_services import logger
from tg_bot.services.message_services import bot_message_service, send_notice
from tg_bot.services.notify_services import HabitNotifyService
from tg_bot.services.redis_services import redis_service
from tg_bot.services.request_services import requests_service
from tg_bot.services.scheduler_services import scheduler_service
from tg_bot.states.states import HabitStates


def register_handlers(bot: TeleBot, settings: Settings) -> None:
    """Регистрируем обработчики команд."""

    @bot.callback_query_handler(
        func=lambda callback: callback.data == "cb_get_all_habits"
    )
    def get_all_habits(callback: CallbackQuery) -> None:
        """Обработчик callback для получения всех привычек пользователя."""
        token = redis_service.load_user_data(user_id=callback.from_user.id, key="token")
        requests_service.set_token_to_session(token=token)
        habits_info: list[dict] = requests_service.get_all_habits_info()
        if habits_info:
            bot.send_message(
                chat_id=callback.message.chat.id,
                text="Вырабатываем привычки:",
                reply_markup=kb_habits_list(habits_info),
            )

    @bot.callback_query_handler(func=lambda callback: callback.data == "cb_add_habit")
    def add_habit(callback: CallbackQuery) -> None:
        """Обработчик callback добавления привычки."""
        msg = bot.send_message(
            chat_id=callback.message.chat.id,
            text="Отправьте название привычки.",
        )
        bot.set_state(
            user_id=callback.from_user.id,
            state=HabitStates.wait_for_habit_name,
            chat_id=callback.message.chat.id,
        )
        bot.register_next_step_handler(msg, get_habit_name)
        bot.answer_callback_query(callback.id)

    def get_habit_name(message: Message) -> None:
        """Получение названия привычки."""
        name = message.text
        logger.debug("Введено название привычки: {}", name)

        bot.add_data(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            name=name,
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
        habit_info = {}
        with bot.retrieve_data(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        ) as data:
            logger.debug("Данные добавляемой привычки: {}", data)
            habit_info.update(data)

        text_parts = (
            f"Название привычки: *{habit_info.get('name')}*",
            f"Описание: *{habit_info.get('description')}*",
            f"Время напоминания: *{habit_info.get('remind_time')}*",
            f"Количество напоминаний: *{habit_info.get('remind_quantity')}*",
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
        habit_info = {}
        with bot.retrieve_data(
            user_id=callback.from_user.id,
            chat_id=callback.message.chat.id,
        ) as data:
            habit_info.update(data)

        habit_info["job_id"] = uuid.uuid4().hex
        habit_info["user_id"] = callback.from_user.id
        habit_info["chat_id"] = callback.message.chat.id

        try:
            habit_data = HabitData(**habit_info)
        except ValidationError as exc:
            logger.error(exc.errors())
            return False

        habit_notify_service = HabitNotifyService(
            logger=logger,
            redis_service=redis_service,
            requests_service=requests_service,
            scheduler_service=scheduler_service,
        )
        success = habit_notify_service.process_notify(func=send_notice, data=habit_data)
        if not success:
            logger.error("Не удалось обработать данные.")
            return False

        bot.delete_state(
            user_id=callback.from_user.id,
            chat_id=callback.message.chat.id,
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

    @bot.callback_query_handler(func=lambda cb: cb.data == "cb_confirm_habit_completed")
    def process_confirm_habit_completed(callback: CallbackQuery) -> None:
        """Подтверждение выполнения привычки."""
        data = callback.json()
        logger.debug("after press button: {}, {}", data, type(data))

        confirm_datetime = datetime.datetime.now(tz=datetime.UTC)
        msg_text = f"Думаем над подтверждением, которое поступило: {confirm_datetime}"

        bot.send_message(
            chat_id=callback.message.chat.id,
            text=msg_text,  # TODO: решить как получить название привычки?
        )
        bot.answer_callback_query(callback.id, text="Осталось ???")
