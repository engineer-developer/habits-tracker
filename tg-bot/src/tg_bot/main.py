"""Модуль запуска бота."""

from aiogram import Bot
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import BotCommand

from tg_bot.configs.app_config import get_settings
from tg_bot.configs.loguru_config import logger
from tg_bot.containers.app_container import AppContainer
from tg_bot.scenes import scenes

# from tg_bot.handlers import router as main_router

app_context = {}


async def setup_bot(bot: Bot):
    """Настройка бота."""
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Профиль пользователя"),
            BotCommand(command="cancel", description="Отмена"),
        ]
    )


async def main() -> None:
    """Функция инициализации хэндлеров и запуска бота."""
    settings = get_settings()
    container = AppContainer()
    container.config.from_pydantic(settings)
    await container.init_resources()

    app_context.update(container=container)

    bot = await container.telegram_bot()
    await setup_bot(bot)

    dp = await container.dispatcher()
    # dp.include_router(main_router)
    scene_registry = SceneRegistry(dp)
    scene_registry.add(*scenes)

    logger.debug("Start bot.")
    await dp.start_polling(bot)
    logger.debug("Stop bot.")

    await bot.session.close()
    await container.shutdown_resources()
