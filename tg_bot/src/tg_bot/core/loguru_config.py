"""Модуль логирования."""

import sys
import loguru


loguru.logger.remove()
logger = loguru.logger
logger.add(
    sink=sys.stderr,
    level="DEBUG",
    format="LOGGER - {time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {module} - {message}",
)
