from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.callbacks.auth import AuthCallback, AuthMethod
from tg_bot.containers.app_container import RedisService, ApiService
from tg_bot.schemas.user_schema import UserLoginSchema
from tg_bot.keyboards.kb_factory import kb_login_or_register, kb_register


router = Router(name=__file__)


@router.message(CommandStart())
async def some(
    message: Message,
    state: FSMContext,
    redis_service: RedisService,
    api_service: ApiService,
):
    """Обработчик команды '/start'."""
    await state.clear()
    token = await redis_service.get_token(telegram_id=message.from_user.id)
    if not token:
        await message.answer(
            text=f"Приветствую {message.from_user.first_name}.\n\n"
            f"Вы не аутентифицированы.\n"
            f"Пожалуйста войдите в систему или зарегистрируйтесь.",
            reply_markup=kb_login_or_register().as_markup(),
        )
        return

    user = await api_service.get_user_profile(token)
    if user:
        await message.answer(f"Привет {user.first_name}!")
        return

    await message.answer(
        "Профиль пользователя не найден.\nНеобходимо зарегистрироваться.",
        reply_markup=kb_register().as_markup(),
    )


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Allow user to cancel any action"""
    current_state = await state.get_state()
    if current_state is None:
        return
    print("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )
