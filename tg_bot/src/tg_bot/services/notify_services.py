from dataclasses import dataclass
from typing import Callable

import loguru
from pydantic import ValidationError

from tg_bot.schemas.habit_schema import HabitAddDto, HabitData, HabitJobDataDto
from tg_bot.services.redis_services import RedisService
from tg_bot.services.request_services import RequestService
from tg_bot.services.scheduler_services import SchedulerService


@dataclass
class HabitNotifyService:
    """Сервис добавления привычки и создания напоминаний о ней."""
    logger: loguru.logger
    redis_service: RedisService
    requests_service: RequestService
    scheduler_service: SchedulerService

    def process_data_for_upload(self, data: HabitData) -> HabitAddDto | None:
        """Готовим данные для отправки."""
        try:
            data = HabitAddDto(**data.model_dump())
            self.logger.debug("Данные, подготовленные для отправки: {}", data)
            return data
        except ValidationError as exc:
            self.logger.debug(exc.errors())

    def process_data_for_job(self, data: HabitData) -> HabitJobDataDto | None:
        """Готовим данные для добавления задания в scheduler."""
        try:
            data = HabitJobDataDto(**data.model_dump())
            self.logger.debug("Данные, подготовленные для создания задания: {}", data)
            return data
        except ValidationError as exc:
            self.logger.debug(exc.errors())

    def process_notify(self, func: Callable, data: HabitData) -> bool:
        """Логика обработки данных.

        - отправляем данные на бэк
        - добавляем задание в scheduler
        """
        token = self.redis_service.load_user_data(user_id=data.user_id, key="token")
        self.logger.debug("Токен полученный из redis: {}", token)
        self.requests_service.set_token_to_session(token=token)
        success_upload = self.requests_service.upload_new_habit_data(
            data=self.process_data_for_upload(data=data)
        )
        if not success_upload:
            self.logger.error("Данные на бэк не отправлены.")
            return False
        success_add_job = self.scheduler_service.create_new_job(
            func=func,
            job_data=self.process_data_for_job(data=data),
        )
        if not success_add_job:
            self.logger.error("Задача на оповещение не добавлена.")
        return True

    def confirm_habit_done(self):
        pass
