from typing import Callable, Optional

from apscheduler.job import Job
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from tg_bot.configs.loguru_config import logger
from tg_bot.schemas.habits import HabitJobCreateCommand


class SchedulerService:
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        self.scheduler = scheduler

    async def create_job(self, func: Callable, cmd: HabitJobCreateCommand) -> Optional[Job]:
        """Создаем новую задачу и добавляем в scheduler."""
        remind_time = cmd.remind_time
        job_trigger = CronTrigger(second="*/30")
        # job_trigger=CronTrigger(
        #     hour=remind_time.hour,
        #     minute=remind_time.minute,
        # ),
        job_id = cmd.habit_id
        job_name = f"Job {cmd.title} {job_id}"

        job = self.scheduler.add_job(
            func=func,
            trigger=job_trigger,
            args=[cmd],
            # kwargs=cmd.model_dump(),
            id=str(job_id),
            name=job_name,
            coalesce=True,
            max_instances=1,
            replace_existing=True,
        )
        if job:
            logger.debug("Добавлена задача id={}", job.id)
            return job

    async def edit_job(self) -> bool:
        """Метод изменения задачи."""
        # TODO: необходимо реализовать
        pass

    async def delete_job(self, job_id: str) -> bool:
        """Метод удаления задачи."""
        try:
            self.scheduler.remove_job(job_id)
            logger.debug(f"Задача с id={job_id} удалена.")
            return True
        except JobLookupError:
            logger.error("Не найдено задачи для удаления.")
            return False
