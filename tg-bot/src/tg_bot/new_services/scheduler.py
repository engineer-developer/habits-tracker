from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerService:
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    def add_job(self, func, **kwargs):
        self.scheduler.add_job(func, **kwargs)
