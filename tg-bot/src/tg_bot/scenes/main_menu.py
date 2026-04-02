from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram.utils.chat_action import ChatActionSender

from tg_bot import callbacks, services, keyboards, scenes, schemas
from tg_bot.configs.loguru_config import logger


class MainMenuScene(
    Scene,
    state="main_menu",
    reset_data_on_enter=True,
    reset_history_on_enter=True,
):
    """Сцена главного меню."""

    async def show_message_with_register_or_login(self, message: Message) -> None:
        """Показывает сообщение с необходимостью
        зарегистрироваться или войти в систему.
        """
        logger.debug("Пользователь не аутентифицирован.")
        await message.answer(
            text="Вы не аутентифицированы.\n"
            "Пожалуйста войдите в систему или зарегистрируйтесь.",
            reply_markup=keyboards.kb_login_or_register(),
        )

    async def show_user_profile(
        self,
        message: Message,
        callback_query: CallbackQuery = None,
    ) -> None:
        """Показывает профиль пользователя."""
        logger.debug("Успешный вход в профиль пользователя.")
        if callback_query and callback_query.data == "back":
            await message.edit_text(
                text="Профиль пользователя", reply_markup=keyboards.kb_profile()
            )
        else:
            await message.answer(
                text="Профиль пользователя", reply_markup=keyboards.kb_profile()
            )

    @on.callback_query.enter()
    async def on_callback_enter(
        self,
        callback_query: CallbackQuery,
        api_service: services.ApiService,
        redis_service: services.RedisService,
    ) -> None:
        await callback_query.answer()
        await self.on_enter(
            message=callback_query.message,
            api_service=api_service,
            redis_service=redis_service,
            callback_query=callback_query,
        )

    @on.message.enter()
    async def on_enter(
        self,
        message: Message,
        api_service: services.ApiService,
        redis_service: services.RedisService,
        callback_query: CallbackQuery = None,
    ) -> None:
        async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
            user_id = (
                callback_query.from_user.id if callback_query else message.from_user.id
            )
            token = await redis_service.get_token(telegram_id=user_id)
            if token is None:
                await self.show_message_with_register_or_login(message)
                return

            user = await api_service.get_user_profile(token)
            if not user:
                await self.show_message_with_register_or_login(message)
                return

            await self.show_user_profile(message, callback_query)

    @on.callback_query(
        callbacks.AuthCallback.filter(F.method == callbacks.AuthMethod.login)
    )
    async def goto_login_scene(self, callback_query: CallbackQuery) -> None:
        """Переход к логину."""
        await callback_query.answer()
        await self.wizard.goto(scenes.LoginScene)

    @on.callback_query(
        callbacks.AuthCallback.filter(F.method == callbacks.AuthMethod.register)
    )
    async def goto_register_scene(self, callback_query: CallbackQuery) -> None:
        """Переход к регистрации."""
        await callback_query.answer()
        await self.wizard.goto(scenes.RegisterScene)

    @on.callback_query(
        callbacks.ProfileMenuCallback.filter(
            F.action == callbacks.ProfileAction.add_habit
        )
    )
    async def goto_add_habit(self, callback_query: CallbackQuery) -> None:
        """Переход к списку активных привычек."""
        await callback_query.answer()
        await self.wizard.goto(scenes.AddHabitTitleInputScene)

    @on.callback_query(
        callbacks.ProfileMenuCallback.filter(
            F.action == callbacks.ProfileAction.non_completed_habits
        )
    )
    async def goto_habits_list_active(self, callback_query: CallbackQuery) -> None:
        """Переход к списку активных привычек."""
        await callback_query.answer()
        await self.wizard.goto(scenes.ActiveHabitsScene)

    @on.callback_query(
        callbacks.ProfileMenuCallback.filter(
            F.action == callbacks.ProfileAction.completed_habits
        )
    )
    async def goto_habits_list_completed(self, callback_query: CallbackQuery) -> None:
        """Переход к списку завершенных привычек."""
        await callback_query.answer()
        await self.wizard.goto(scenes.CompletedHabitsScene)
