"""Модуль планировщика задач."""

import datetime
from dataclasses import dataclass
from typing import Callable, Optional

import loguru
from apscheduler.jobstores.base import BaseJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from tg_bot.schemas.habit_schema import HabitDataDto
from tg_bot.services.logging_services import logger


@dataclass
class SchedulerBuilder(BackgroundScheduler):
    """Класс планировщика."""

    job_store: BaseJobStore
    jobstores: Optional[dict] = None
    timezone: Optional[datetime.tzinfo] = None

    def __post_init__(self) -> None:
        """Логика инициализации и запуск планировщика."""
        self.jobstores = {"default": self.job_store}
        self.timezone = datetime.UTC
        super().__init__(jobstores=self.jobstores, timezone=self.timezone)


@dataclass
class SchedulerService:
    """Сервис планировщика задач."""

    scheduler: SchedulerBuilder
    logger: loguru.logger

    def create_new_job(self, func: Callable, job_data: HabitDataDto) -> bool:
        """Создаем новую задачу и добавляем в scheduler."""
        remind_time = job_data.remind_time
        name = job_data.name
        job_id = job_data.job_id

        job = self.scheduler.add_job(
            func=func,
            trigger=CronTrigger(second="*/30"),
            # trigger=CronTrigger(
            #     hour=remind_time.hour,
            #     minute=remind_time.minute,
            # ),
            kwargs=job_data.model_dump(),
            id=job_id,
            name=f"Job_{name}",
            coalesce=True,
            max_instances=1,
            replace_existing=True,
        )
        if job:
            self.logger.debug("Задача '{}' добавлена", job.id)
            self.scheduler.print_jobs()
            return True
        else:
            return False


redis_job_store = RedisJobStore(db=0)
scheduler = SchedulerBuilder(job_store=redis_job_store)
scheduler_service = SchedulerService(scheduler=scheduler, logger=logger)
