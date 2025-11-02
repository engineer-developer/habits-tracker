from typing import Callable

from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.cron import CronTrigger
from pydantic import ValidationError

from tg_bot.services.logging_services import logger
from tg_bot.schemas.habit_schema import HabitJobDataDto

#
# def add_notice_job(scheduler: BaseScheduler, func: Callable, job_data: dict) -> bool:
#     """Добавляем задачу в scheduler."""
#     try:
#         job_data = HabitJobDataDto(**job_data)
#     except ValidationError as exc:
#         logger.error(exc.errors())
#         return False
#
#     remind_time = job_data.remind_time
#     name = job_data.name
#     job_id = job_data.job_id
#
#     job = scheduler.add_job(
#         func=func,
#         trigger=CronTrigger(second="*/30"),
#         # trigger=CronTrigger(
#         #     hour=remind_time.hour,
#         #     minute=remind_time.minute,
#         # ),
#         kwargs=job_data.model_dump(),
#         id=job_id,
#         name=f"Job_{name}",
#         coalesce=True,
#         max_instances=1,
#         replace_existing=True,
#     )
#     if job:
#         logger.debug("Задача '{}' добавлена", job.id)
#         scheduler.print_jobs()
#         return True
#     else:
#         return False
