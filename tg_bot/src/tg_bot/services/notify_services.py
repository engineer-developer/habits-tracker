"""Модуль сервиса напоминаний о необходимости выполнения привычки."""

from dataclasses import dataclass
from typing import Callable

import loguru
from pydantic import ValidationError

from tg_bot.schemas.habit_schema import HabitAddDto, HabitDataDto
from tg_bot.services.logging_services import logger
from tg_bot.services.redis_services import RedisService, redis_service
from tg_bot.services.request_services import (
    RequestService,
    TokenAuthSessionStrategy,
    requests_service,
)
from tg_bot.services.scheduler_services import SchedulerService, scheduler_service


@dataclass
class HabitNotifyService:
    """Сервис добавления привычки и создания напоминаний о ней."""

    logger: loguru.logger
    redis_service: RedisService
    requests_service: RequestService
    scheduler_service: SchedulerService

    def process_data_for_upload(self, data: HabitDataDto) -> HabitAddDto | None:
        """Готовим данные для отправки на бэкэнд."""
        try:
            data = HabitAddDto(**data.model_dump())
            self.logger.debug("Данные, подготовленные для отправки: {data}", data=data)
            return data
        except ValidationError as exc:
            self.logger.debug(exc.errors())

    def process_notify(self, func: Callable, data: HabitDataDto) -> bool:
        """Логика обработки данных.

        - Отправляем данные на бэк.
        - Добавляем задание в scheduler.
        """
        token = self.redis_service.load_user_data(user_id=data.user_id, key="token")
        self.requests_service.strategy = TokenAuthSessionStrategy(token=token)

        success_upload = self.requests_service.upload_new_habit_data(
            data=self.process_data_for_upload(data=data)
        )
        if not success_upload:
            self.logger.error("Данные на бэк не отправлены.")
            return False

        success_add_job = self.scheduler_service.create_new_job(
            func=func,
            job_data=data,
        )
        if not success_add_job:
            self.logger.error("Задача на оповещение не добавлена.")
            return False

        return True


habit_notify_service = HabitNotifyService(
    logger=logger,
    redis_service=redis_service,
    requests_service=requests_service,
    scheduler_service=scheduler_service,
)
