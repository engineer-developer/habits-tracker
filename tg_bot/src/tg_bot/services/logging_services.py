"""Модуль создания и инициализации сервиса логирования."""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Optional

import loguru

from tg_bot.core.config import settings


@dataclass
class LoggingService:
    """Сервис логирования."""

    FORMAT: ClassVar[str] = (
        "LOGGER - {time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {module} - {message}"
    )

    log_level: str
    logger: Optional[loguru.logger] = None

    def __post_init__(self) -> None:
        """Логика инициализации."""
        if not self.logger:
            loguru.logger.remove()
            self.logger = loguru.logger

            self.logger.add(
                sink=sys.stderr,
                level=self.log_level,
                format=self.FORMAT,
            )

            log_file = Path(__file__).parent.parent / "logs" / "app.log"
            self.logger.add(
                sink=log_file,
                level="DEBUG",
                format=self.FORMAT,
            )


logging_service = LoggingService(log_level=settings.logging_level)
logger = logging_service.logger
