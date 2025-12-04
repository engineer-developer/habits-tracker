"""Модуль запуска бота."""

from tg_bot.core.bot_factory import bot
from tg_bot.core.config import settings
from tg_bot.handlers import register_handlers
from tg_bot.service_layer.logging_service import logger
from tg_bot.service_layer.scheduler_service import scheduler


def main() -> None:
    """Функция инициализации хэндлеров и запуска бота."""
    register_handlers(bot, settings)
    logger.debug("Start bot.")
    scheduler.start()
    scheduler.print_jobs()
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
