"""Модуль запуска бота."""


from aiogram.types import BotCommand

from tg_bot.configs.app_config import get_settings
from tg_bot.configs.loguru_config import logger
from tg_bot.containers.app_container import AppContainer
from tg_bot.handlers import router as main_router


async def main() -> None:
    """Функция инициализации хэндлеров и запуска бота."""
    settings = get_settings()
    container = AppContainer()
    container.config.from_pydantic(settings)
    await container.init_resources()

    # scheduler = container.scheduler()
    redis_service = await container.redis_service()
    api_service = await container.api_service()

    bot = await container.telegram_bot()
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Профиль пользователя"),
            BotCommand(command="cancel", description="Отмена"),
        ]
    )
    dp = await container.dispatcher(
        redis_service=redis_service,
        api_service=api_service,
    )
    dp.include_router(main_router)

    logger.debug("Start bot.")
    await dp.start_polling(bot)
    logger.debug("Stop bot.")

    await container.shutdown_resources()
