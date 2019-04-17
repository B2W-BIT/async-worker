from asyncworker.base import BaseApp
from asyncworker.consumer import Consumer  # noqa: F401
from asyncworker.options import (  # noqa: F401
    Options,
    DefaultValues,
    Events,
    RouteTypes,
)
from asyncworker.signals.handlers.http import HTTPServer
from asyncworker.signals.handlers.rabbitmq import RabbitMQ


class App(BaseApp):
    handlers = (RabbitMQ(), HTTPServer())

    def __init__(
        self, host: str, user: str, password: str, prefetch_count: int = None
    ) -> None:
        super(App, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.prefetch_count = prefetch_count
