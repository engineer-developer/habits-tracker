import sys
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Optional

import loguru


@dataclass
class LoggingService:
    """Сервис логгирования."""

    LOG_LEVEL: ClassVar[str] = "DEBUG"
    FORMAT: ClassVar[str] = (
        "LOGGER - {time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {module} - {message}"
    )

    logger: Optional[loguru.logger] = None

    def __post_init__(self) -> None:
        """Логика инициализации."""
        if not self.logger:
            loguru.logger.remove()
            self.logger = loguru.logger

            self.logger.add(
                sink=sys.stderr,
                level=self.LOG_LEVEL,
                format=self.FORMAT,
            )

            log_file = Path(__file__).parent.parent / "logs" / "app.log"
            self.logger.add(
                sink=log_file,
                level=self.LOG_LEVEL,
                format=self.FORMAT,
            )


logging_service = LoggingService()
logger = logging_service.logger
