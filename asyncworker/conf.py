import logging

from pydantic import BaseSettings
from simple_json_logger import JsonLogger


class Settings(BaseSettings):
    LOGLEVEL: str = "ERROR"

    HTTP_ENABLED: bool = True
    HTTP_HOST: str = 'localhost'
    HTTP_PORT: int = 8080

    AMQP_DEFAULT_VHOST: str = '/'

    class Config:
        allow_mutation = False
        env_prefix = "ASYNCWORKER_"


settings = Settings()

logger = JsonLogger(flatten=True)
logger.setLevel(getattr(logging, settings.LOGLEVEL, logging.INFO))
