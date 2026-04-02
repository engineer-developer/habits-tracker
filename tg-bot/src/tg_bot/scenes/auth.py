from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from tg_bot import callbacks, keyboards, scenes, schemas, services
from tg_bot.configs.loguru_config import logger


class LoginScene(Scene, state="login_state"):
    @on.callback_query.enter()
    async def on_callback_enter(self, callback_query: CallbackQuery):
        
        await callback_query.answer()
        await callback_query.message.edit_text(
            text="Введите пароль для аутентификации...",
        )

    @on.message(CommandStart())
    async def goto_main_menu(self, message: Message):
        await self.wizard.goto(scenes.MainMenuScene)

    @on.message(F.text)
    async def get_password(
        self,
        message: Message,
        api_service: services.ApiService,
        redis_service: services.RedisService,
    ):
        """Получаем пароль и входим в систему через api."""
        password = message.text
        credentials = schemas.UserCredentials(
            telegram_id=message.from_user.id,
            password=password,
        )
        token = await api_service.login(credentials)
        if token is None:
            await message.answer(
                text="Не удалось войти в систему.\n"
                "Попробуйте повторно ввести пароль или зарегистрируйтесь /start",
            )
            return

        await redis_service.save_token(
            telegram_id=message.from_user.id,
            value=token,
        )
        user: schemas.UserRead = await api_service.get_user_profile(token)
        if not user:
            await message.edit_text(
                text="Не удалось войти в систему.\n"
                "Попробуйте повторно ввести пароль или зарегистрируйтесь /start"
            )
            return

        await self.wizard.back()


class RegisterScene(Scene, state="register_state"):
    @on.callback_query.enter()
    async def on_callback_enter(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.message.enter()
    async def on_enter(self, message: Message):
        await message.answer("Введите пароль для регистрации...")

    @on.message(F.text)
    async def get_password(
        self,
        message: Message,
        api_service: services.ApiService,
        redis_service: services.RedisService,
    ):
        """Получаем пароль и регистрируем пользователя через api."""
        password = message.text
        user = schemas.UserCreateCommand(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            password=password,
        )
        token = await api_service.register(user)
        if token is None:
            await message.answer("Не удалось зарегистрировать пользователя.")
            await self.wizard.back()
            return

        await redis_service.save_token(
            telegram_id=message.from_user.id,
            value=token,
        )
        await message.answer(
            text="Вы успешно зарегистрированы.\nПожалуйста войдите в систему",
            reply_markup=keyboards.kb_login(),
        )

    @on.callback_query(
        callbacks.AuthCallback.filter(F.method == callbacks.AuthMethod.login)
    )
    async def goto_login_scene(self, callback_query: CallbackQuery):
        """Переход к логину."""
        await callback_query.answer()
        await self.wizard.goto(LoginScene)
