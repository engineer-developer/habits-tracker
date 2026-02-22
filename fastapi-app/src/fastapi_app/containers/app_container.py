from database.database import Database
from dependency_injector import containers, providers
from repositories.users import UserRepository
from services import UserService, AuthService


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

    user_service = providers.Factory(
        UserService,
        repository=user_repository,
    )

    auth_service = providers.Factory(
        AuthService,
        secret_key=config.auth.secret_key,
        algorithm=config.auth.algorithm,
        access_token_expire_minutes=config.auth.access_token_expire_minutes,
        user_service=user_service,
    )
