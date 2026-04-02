"""Модуль запуска бота."""

from aiogram import Bot, Dispatcher
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import BotCommand

from tg_bot.configs.app_config import get_settings
from tg_bot.configs.loguru_config import logger
from tg_bot.containers.app_container import AppContainer
from tg_bot.routers import router
from tg_bot.scenes import scenes


async def setup_bot(bot: Bot) -> None:
    """Настройка бота."""
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Профиль пользователя"),
        ]
    )


async def main() -> None:
    """Функция инициализации хэндлеров и запуска бота."""
    settings = get_settings()
    container = AppContainer()
    container.config.from_pydantic(settings)
    container.wire(
        modules=["tg_bot.utils.notify"],
    )
    await container.init_resources()

    dp: Dispatcher = await container.dispatcher()

    scene_registry = SceneRegistry(dp)
    scene_registry.add(*scenes)

    bot: Bot = await container.telegram_bot()
    await setup_bot(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(router)

    logger.debug("Start bot.")
    await dp.start_polling(bot)
    logger.debug("Stop bot.")

    await bot.session.close()
    await container.shutdown_resources()
