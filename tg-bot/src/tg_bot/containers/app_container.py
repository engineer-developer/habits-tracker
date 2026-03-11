import httpx
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import SimpleEventIsolation, DisabledEventIsolation
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector import containers, providers
from redis.asyncio import client

from tg_bot.services.api import ApiService
from tg_bot.services.redis import RedisService
from tg_bot.services.scheduler import SchedulerService


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    redis_client = providers.Resource(
        client.Redis,
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        decode_responses=True,
    )

    redis_storage = providers.Resource(
        RedisStorage,
        redis=redis_client,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    http_client = providers.Resource(
        httpx.AsyncClient,
        base_url=config.api.url,
        timeout=5,
    )

    telegram_bot = providers.Resource(
        Bot,
        token=config.bot.token,
    )

    @staticmethod
    async def _init_scheduler():
        scheduler = AsyncIOScheduler()
        scheduler.add_jobstore(
            "redis",
            jobs_key="jobs",
            run_times_key="run_times",
        )
        scheduler.start()
        return scheduler

    scheduler = providers.Resource(_init_scheduler)

    scheduler_service = providers.Factory(
        SchedulerService,
        scheduler=scheduler,
    )
    redis_service = providers.Factory(
        RedisService,
        client=redis_client,
    )

    api_service = providers.Factory(
        ApiService,
        client=http_client,
    )

    dispatcher = providers.Factory(
        Dispatcher,
        storage=redis_storage,
        bot=telegram_bot,
        api_service=api_service,
        redis_service=redis_service,
        scheduler_service=scheduler_service,
    )
