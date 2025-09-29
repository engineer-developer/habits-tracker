from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field


class Settings(BaseSettings):
    """
    Настройки сервиса
    """

    db_url: PostgresDsn = Field(validation_alias="DB_URL")


settings = Settings()
