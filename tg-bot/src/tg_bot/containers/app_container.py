import httpx
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector import containers, providers
from redis.asyncio import client

from tg_bot.new_services.api import ApiService
from tg_bot.new_services.redis import RedisService
from tg_bot.new_services.scheduler import SchedulerService


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

    dispatcher = providers.Factory(
        Dispatcher,
        bot=telegram_bot,
        storage=redis_storage,
    )

    @staticmethod
    async def _init_scheduler():
        scheduler = AsyncIOScheduler(timezone="UTC")
        scheduler.start()
        try:
            yield scheduler
        finally:
            scheduler.shutdown()

    scheduler = providers.Resource(_init_scheduler)

    redis_service = providers.Factory(
        RedisService,
        client=redis_client,
    )

    api_service = providers.Factory(
        ApiService,
        client=http_client,
    )

    scheduler_service = providers.Factory(
        SchedulerService,
        scheduler=scheduler,
    )
