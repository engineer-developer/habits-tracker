from core.bot_factory import bot
from core.loguru_config import logger
from handlers.command_handlers import process_start


def main():
    """Запуск бота."""
    bot.register_message_handler(process_start, commands=["start"], pass_bot=True)

    logger.debug("Start bot.")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
