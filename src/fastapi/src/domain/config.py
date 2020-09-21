import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = os.getenv("APP_ENV", "local-dev")
    MYSQL_PRIMARY_HOST: str = os.getenv("MYSQL_PRIMARY_HOST", "ntv-giants.db")
    MYSQL_REPLICA_HOST: str = os.getenv("MYSQL_REPLICA_HOST", "ntv-giants.db")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "giants")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "giants")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "giants")
    CACHE_HOST: str = os.getenv("CACHE_HOST", "ntv-giants.cache")
    TIMEZONE: str = "Asia/Tokyo"


settings = Settings()
