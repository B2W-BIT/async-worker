from enum import Enum, auto
from typing import List


class AutoNameEnum(str, Enum):
    def _generate_next_value_(  # type: ignore
        name: str, start: int, count: int, last_values: List[str]
    ) -> str:
        return name.lower()


class Options(AutoNameEnum):
    BULK_SIZE = auto()
    BULK_FLUSH_INTERVAL = auto()
    MAX_CONCURRENCY = auto()
    CONNECTION_FAIL_CALLBACK = auto()


class Actions(AutoNameEnum):
    ACK = auto()
    REJECT = auto()
    REQUEUE = auto()


class Events(AutoNameEnum):
    ON_SUCCESS = auto()
    ON_EXCEPTION = auto()


class DefaultValues:
    BULK_SIZE = 1
    BULK_FLUSH_INTERVAL = 60
    ON_SUCCESS = Actions.ACK
    ON_EXCEPTION = Actions.REQUEUE
    RUN_EVERY_MAX_CONCURRENCY = 1


class RouteTypes(AutoNameEnum):
    AMQP_RABBITMQ = auto()
    HTTP = auto()
