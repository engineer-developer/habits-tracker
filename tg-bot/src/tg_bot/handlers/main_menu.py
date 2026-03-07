"""Обработчик первичного взаимодействия с ботом."""

from aiogram.dispatcher.router import Router
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)

from tg_bot.configs.loguru_config import logger
from tg_bot.containers.app_container import ApiService, RedisService
from tg_bot.keyboards.kb_factory import kb_login_or_register, kb_profile

router = Router(name="main_menu")


async def show_user_profile(message: Message) -> None:
    """Показывает профиль пользователя."""
    logger.debug("Успешный вход в профиль пользователя.")
    await message.answer(f"Профиль пользователя", reply_markup=kb_profile())


async def show_message_with_register_or_login(message: Message) -> None:
    """Показывает сообщение с необходимостью
    зарегистрироваться или войти в систему.
    """
    await message.answer(
        text=f"Вы не аутентифицированы.\n"
        f"Пожалуйста войдите в систему или зарегистрируйтесь.",
        reply_markup=kb_login_or_register(),
    )


@router.message(CommandStart())
async def index(
    message: Message,
    state: FSMContext,
    redis_service: RedisService,
    api_service: ApiService,
) -> None:
    """Обработчик команды /start."""
    await state.clear()
    token = await redis_service.get_token(telegram_id=message.from_user.id)

    if not token:
        logger.error("Токен не найден.")
        await show_message_with_register_or_login(message)
        return

    user = await api_service.get_user_profile(token)

    if not user:
        logger.error("Данные пользователя не получены.")
        await show_message_with_register_or_login(message)
        return

    await show_user_profile(message)


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Позволяет отменить любые действия."""
    await state.clear()
    logger.debug(f"Сброс состояния")
    await message.answer(
        "Отменено. Отправьте /start", reply_markup=ReplyKeyboardRemove()
    )
