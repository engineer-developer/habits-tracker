"""Модуль сервиса напоминаний о необходимости выполнения привычки."""

from dataclasses import dataclass
from typing import Callable

import loguru
from pydantic import ValidationError

from schemas.habits import HabitAddDto, HabitDataDto
from services.logging_service import logger
from services.redis_service import RedisService, redis_service
from services.request_service import (
    RequestService,
    TokenAuthSessionStrategy,
    requests_service,
)
from services.scheduler_service import SchedulerService, scheduler_service


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
            self.logger.debug("Данные, подготовленные для отправки: {}", data)
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

        habit_data = self.requests_service.upload_new_habit_data(
            data=self.process_data_for_upload(data=data)
        )
        if habit_data is None:
            self.logger.error("Данные на бэк не отправлены.")
            return False

        success_add_job = self.scheduler_service.create_job(
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
