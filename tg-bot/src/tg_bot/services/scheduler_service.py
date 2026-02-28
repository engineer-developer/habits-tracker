"""Модуль планировщика задач."""

import datetime
from dataclasses import dataclass
from typing import Callable, Optional

import loguru
from apscheduler.jobstores.base import BaseJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from schemas.habits import HabitDataDto
from services.logging_service import logger


@dataclass
class SchedulerBuilder(BackgroundScheduler):
    """Класс планировщика."""

    def __init__(self, job_store: BaseJobStore):
        """Логика инициализации планировщика."""
        self.job_store = job_store
        self.jobstores = {"default": self.job_store}
        self.timezone = datetime.UTC
        super().__init__(jobstores=self.jobstores, timezone=self.timezone)


class SchedulerService:
    """Сервис планировщика задач."""

    def __init__(self, scheduler: SchedulerBuilder, logger: loguru.logger) -> None:
        """Логика инициализации."""
        self.scheduler = scheduler
        self.logger = logger

    def create_job(self, func: Callable, job_data: dict) -> bool:
        """Создаем новую задачу и добавляем в scheduler."""
        remind_time = job_data.get("remind_time")
        title = job_data.get("title")
        job_id = job_data.get("id")
        job_name = f"Job_{title}_{job_id}"
        job_trigger = CronTrigger(second="*/30")
        # job_trigger=CronTrigger(
        #     hour=remind_time.hour,
        #     minute=remind_time.minute,
        # ),

        job = self.scheduler.add_job(
            func=func,
            trigger=job_trigger,
            kwargs=job_data,
            id=job_id,
            name=job_name,
            coalesce=True,
            max_instances=1,
            replace_existing=True,
        )
        if job:
            self.logger.debug("Добавлена задача {}", job.id)
            self.scheduler.print_jobs()
            return True
        else:
            return False

    def edit_job(self):
        """Метод изменения задачи."""
        pass

    def delete_job(self):
        """Метод удаления задачи."""
        pass

redis_job_store = RedisJobStore(db=0)
scheduler = SchedulerBuilder(job_store=redis_job_store)

scheduler_service = SchedulerService(scheduler=scheduler, logger=logger)
