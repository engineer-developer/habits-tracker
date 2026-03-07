"""Обработчик входа в систему."""

from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from tg_bot.callbacks.auth import AuthCallback, AuthMethod
from tg_bot.handlers.main_menu import show_user_profile
from tg_bot.services.api import ApiService
from tg_bot.services.redis import RedisService
from tg_bot.schemas.users import UserCredentials, UserRead
from tg_bot.states.states import AuthStates

router = Router(name="login")


@router.callback_query(AuthCallback.filter(F.method == AuthMethod.login))
async def register_user(callback: CallbackQuery, state: FSMContext):
    """Начинаем флоу входа в систему."""
    await state.set_state(AuthStates.wait_password_for_login)
    await callback.answer()
    await callback.message.answer("Введите пароль для аутентификации...")


@router.message(AuthStates.wait_password_for_login, F.text)
async def get_password_for_register(
    message: Message,
    state: FSMContext,
    api_service: ApiService,
    redis_service: RedisService,
):
    """Получаем пароль и входим в систему через api."""
    password = message.text
    credentials = UserCredentials(
        telegram_id=message.from_user.id,
        password=password,
    )
    token = await api_service.login(credentials)

    if not token:
        await message.answer(
            "Не удалось войти в систему.\n"
            "Попробуйте повторно ввести пароль или зарегистрируйтесь /start"
        )
        return

    await redis_service.save_token(
        telegram_id=message.from_user.id,
        value=token,
    )
    user: UserRead = await api_service.get_user_profile(token)

    if not user:
        await message.answer(
            "Не удалось войти в систему.\n"
            "Попробуйте повторно ввести пароль или зарегистрируйтесь /start"
        )
        return

    await state.clear()
    await show_user_profile(message)
