from datetime import time
from typing import Optional

from aiogram.types import Message
from pydantic import ValidationError

from tg_bot import schemas, keyboards
from tg_bot.configs.loguru_config import logger


class ValidateTitleMixin:
    """Миксин для валидации названия привычки."""

    @staticmethod
    async def validate_title(message: Message) -> Optional[str]:
        try:
            title = schemas.HabitTitleInput(title=message.text).title
            logger.debug(f"Введено название привычки: {title}")
            return title
        except ValidationError as exc:
            logger.error(f"{exc}")
            await message.answer(
                text="Неверно указано название.\n"
                "Используйте только буквы, цифры, пробел, дефис, двоеточие",
                reply_markup=keyboards.kb_back_cancel(),
            )


class ValidateDescriptionMixin:
    """Миксин для валидации описания привычки."""

    @staticmethod
    async def validate_description(message: Message) -> Optional[str]:
        try:
            description = schemas.HabitDescriptionInput(
                description=message.text
            ).description
            logger.debug(f"Введено описание привычки: {description}")
            return description
        except ValidationError as exc:
            logger.error(f"{exc}")
            await message.answer(
                text="Неверно указано описание.\n"
                "Используйте только буквы, цифры, пробел, дефис, двоеточие",
                reply_markup=keyboards.kb_back_cancel(),
            )


class ValidateRemindTimeMixin:
    """Миксин для валидации описания привычки."""

    @staticmethod
    async def validate_remind_time(message: Message) -> Optional[str]:
        try:
            input_value = schemas.HabitRemindTimeInput(
                remind_time=time.fromisoformat(message.text)
            )
            remind_time = input_value.remind_time.strftime("%H:%M:%S")
            logger.debug(f"Введено время: {remind_time}")
            return remind_time
        except (ValueError, ValidationError) as exc:
            logger.error(f"{exc}")
            await message.answer(
                text="Не верно указано время.\nУкажите в формате: ЧЧ:ММ",
                reply_markup=keyboards.kb_back_cancel(),
            )


class ValidateRemindQuantityMixin:
    """Миксин для валидации описания привычки."""

    @staticmethod
    async def validate_remind_quantity(message: Message) -> Optional[int]:
        try:
            remind_quantity = schemas.HabitRemindQuantityInput(
                remind_quantity=int(message.text)
            ).remind_quantity
            logger.debug(f"Введено количество напоминаний: {remind_quantity}")
            return remind_quantity
        except (ValueError, ValidationError) as exc:
            logger.error(f"{exc}")
            await message.answer(
                text=f"Не верно указано количество.\n"
                "Укажите целое положительное число.",
                reply_markup=keyboards.kb_back_cancel(),
            )
