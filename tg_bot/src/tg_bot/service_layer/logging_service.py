"""Модуль создания и инициализации сервиса логирования."""

import sys
from pathlib import Path

import loguru

from tg_bot.core.config import settings


class LoggingService:
    """Сервис логирования."""

    FORMAT: str = (
        "LOGGER - {time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {module} - {message}"
    )
    LOG_FILE_PATH: Path = Path(__file__).parent.parent / "logs" / "app.log"

    def __init__(self, log_level: str):
        self.log_level = log_level
        self.logger = self._init_logger()

    def _init_logger(self):
        """Логика инициализации логера."""
        loguru.logger.remove()
        logger = loguru.logger

        logger.add(
            sink=sys.stderr,
            level=self.log_level,
            format=self.FORMAT,
        )

        logger.add(
            sink=self.LOG_FILE_PATH,
            level="DEBUG",
            format=self.FORMAT,
        )
        return logger


logging_service = LoggingService(log_level=settings.logging_level)
logger = logging_service.logger
