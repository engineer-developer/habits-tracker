"""Модуль запуска бота."""

from core.bot_factory import bot
from core.config import Settings, get_settings
from core.loguru_config import logger
from handlers import register_handlers
from telebot import TeleBot


def main(bot: TeleBot, settings: Settings) -> None:
    """Функция инициализации хэндлеров и запуска бота."""
    register_handlers(bot, settings)
    logger.debug("Start bot.")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    settings = get_settings()
    main(bot=bot, settings=settings)
