import logging
import time
from typing import List

from aiologger.loggers.json import JsonLogger
from pydantic import BaseSettings

from asyncworker.options import DefaultValues

INFINITY = float("inf")


class Settings(BaseSettings):
    LOGLEVEL: str = "ERROR"

    AMQP_DEFAULT_VHOST: str = "/"
    AMQP_DEFAULT_PREFETCH_COUNT: int = 128
    AMQP_DEFAULT_HEARTBEAT: int = 60

    HTTP_HOST: str = "127.0.0.1"
    HTTP_PORT: int = 8080

    FLUSH_TIMEOUT: int = DefaultValues.BULK_FLUSH_INTERVAL

    # metrics
    METRICS_ENDPOINT: str = "/metrics"
    METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS: List[float] = [
        10,
        50,
        100,
        200,
        500,
        1_000,
        5_000,
        INFINITY,
    ]

    class Config:
        allow_mutation = False
        env_prefix = "ASYNCWORKER_"


default_timer = time.perf_counter
settings = Settings()

loglevel = getattr(logging, settings.LOGLEVEL, logging.INFO)
logger = JsonLogger.with_default_handlers(level=loglevel, flatten=True)
