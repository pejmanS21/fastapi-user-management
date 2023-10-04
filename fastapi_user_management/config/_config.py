"""Fastapi application config."""

from omegaconf import OmegaConf
from pydantic import EmailStr
from pydantic_settings import BaseSettings

from fastapi_user_management import __version__

APP_CUSTOM_CONFIG = OmegaConf.load("settings.yaml")


class Settings(BaseSettings):
    SECRET_KEY: str

    ADMIN_FULLNAME: str
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str

    TITLE: str = APP_CUSTOM_CONFIG.fastapi.title
    DESCRIPTION: str = APP_CUSTOM_CONFIG.fastapi.description

    VERSION: str = __version__

    DOCS_URL: str = APP_CUSTOM_CONFIG.fastapi.docs_url
    REDOC_URL: str = APP_CUSTOM_CONFIG.fastapi.redoc_url

    ALGORITHM: str = APP_CUSTOM_CONFIG.fastapi.algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        APP_CUSTOM_CONFIG.fastapi.access_token_expire_minutes
    )

    DATABASE_URI: str = APP_CUSTOM_CONFIG.database.uri

    class Config:
        env_file = ".env"
        case_sensitive = True


SETTINGS = Settings()
