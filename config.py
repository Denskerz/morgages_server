import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    ENV: str = "development"

    # JWT_SECRET_KEY: str = None
    # JWT_ALGORITHM: str = None
    # CELERY_BROKER_URL: str
    # CELERY_BACKEND_URL: str
    # REDIS_HOST: str
    # REDIS_PORT: int
    # API_KEY_PREFIX: str = "API_KEY_"
    ECHO_SQL: bool = True
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_SCHEMA: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


class IFTSettings(Settings):
    pass


class PSISettings(Settings):
    pass


class PROMSettings(Settings):
    pass


def get_config():
    """
    берем разные env файлы в зависимости от стенда(psi/prom/ift)
    :return:
    """
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": IFTSettings(),
        "local": PSISettings(),
        "prod": PROMSettings(),
    }
    return config_type[env]


settings: Settings = get_config()
