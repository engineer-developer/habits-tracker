"""Модуль логирования."""

# import sys
# from pathlib import Path
#
# import loguru
#
#
# LOG_LEVEL = "DEBUG"
# FORMAT = "LOGGER - {time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {module} - {message}"
#
#
# loguru.logger.remove()
# logger = loguru.logger
#
# logger.add(
#     sink=sys.stderr,
#     level=LOG_LEVEL,
#     format=FORMAT,
# )
#
# log_file = Path(__file__).parent.parent / "logs" / "app.log"
# logger.add(
#     sink=log_file,
#     level=LOG_LEVEL,
#     format=FORMAT,
# )
