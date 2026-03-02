from dependency_injector import containers, providers

from fastapi_app.database.database import Database
from fastapi_app.repositories.habits import HabitRepository
from fastapi_app.repositories.tracking import TrackingRepository
from fastapi_app.repositories.users import UserRepository
from fastapi_app.services.auth import AuthService
from fastapi_app.services.habits import HabitService
from fastapi_app.services.tracking import TrackingService
from fastapi_app.services.users import UserService


class AppContainer(containers.DeclarativeContainer):
    """Основной контейнер."""

    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        drivername="postgresql+asyncpg",
        username=config.db.user,
        password=config.db.passw,
        host=config.db.host,
        port=config.db.port,
        database=config.db.name,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    habit_repository = providers.Factory(
        HabitRepository,
        session_factory=db.provided.session,
    )
    tracking_repository = providers.Factory(
        TrackingRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        repository=user_repository,
    )

    habit_service = providers.Factory(
        HabitService,
        repository=habit_repository,
    )

    tracking_service = providers.Factory(
        TrackingService,
        repository=tracking_repository,
        habit_service=habit_service,
    )

    auth_service = providers.Factory(
        AuthService,
        secret_key=config.auth.secret_key,
        algorithm=config.auth.algorithm,
        access_token_expire_minutes=config.auth.access_token_expire_minutes,
        user_service=user_service,
    )
