from enum import Enum, auto


class Options(Enum):
    BULK_SIZE = auto()
    BULK_FLUSH_INTERVAL = auto()

class Actions(Enum):
    ACK = auto()
    REJECT = auto()
    REQUEUE = auto()


class Events(Enum):
    ON_SUCCESS = auto()
    ON_EXCEPTION = auto()


class Defaultvalues:
    BULK_SIZE = 1
    BULK_FLUSH_INTERVAL = 60
    ON_SUCCESS = Actions.ACK
    ON_EXCEPTION = Actions.REQUEUE
