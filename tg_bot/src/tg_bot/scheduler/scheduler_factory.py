import datetime

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from tg_bot.core.config import settings


# redis_job_store = RedisJobStore(db=0)
#
# jobstores = {"default": redis_job_store}
#
# scheduler = BackgroundScheduler(
#     jobstores=jobstores,
#     timezone=datetime.UTC,
# )
# scheduler.start()


# def some_task(a: int, b: int):
#     print(datetime.datetime.now(timezone.utc))
#     print("a+b=", a + b)
#
#
# job = scheduler.add_job(
#     func=some_task,
#     trigger=CronTrigger(second="*/5"),
#     args=[],
#     kwargs=dict(a=2, b=3),
#     id="some_unique_id",
#     name="SuperJobName",
#     coalesce=True,
#     max_instances=1,
#     replace_existing=True,
# )
#
#
# while True:
#     time.sleep(1)
