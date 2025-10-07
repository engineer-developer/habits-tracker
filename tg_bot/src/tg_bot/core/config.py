from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    bot_token: str = Field(validation_alias="BOT_TOKEN")
    api_url: str = Field(validation_alias="FASTAPI_API_URL")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env"
    )


def get_settings():
    return Settings()