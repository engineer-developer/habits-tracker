"""Обработчик регистрации пользователя."""

from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery

from tg_bot.callbacks.auth import AuthCallback, AuthMethod
from tg_bot.keyboards.kb_factory import kb_login
from tg_bot.services.api import ApiService
from tg_bot.services.redis import RedisService
from tg_bot.schemas.users import UserCreateCommand
from tg_bot.states.states import AuthStates

router = Router(name="register")


@router.callback_query(AuthCallback.filter(F.method == AuthMethod.register))
async def register_user(callback: CallbackQuery, state: FSMContext) -> None:
    """Начинаем флоу регистрации."""
    await state.set_state(AuthStates.wait_password_for_register)
    await callback.answer()
    await callback.message.answer("Введите пароль для регистрации...")


@router.message(AuthStates.wait_password_for_register, F.text)
async def get_password_for_register(
    message: Message,
    state: FSMContext,
    api_service: ApiService,
    redis_service: RedisService,
) -> None:
    """Получаем пароль и регистрируем пользователя через api."""
    password = message.text
    user = UserCreateCommand(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        password=password,
    )

    token = await api_service.register(user)
    if not token:
        await message.answer(
            "Не удалось зарегистрировать пользователя.\nНажмите /start"
        )
        return

    await redis_service.save_token(
        telegram_id=message.from_user.id,
        value=token,
    )
    await message.answer(
        text="Вы успешно зарегистрированы.\nПожалуйста войдите в систему",
        reply_markup=kb_login(),
    )
    await state.clear()
