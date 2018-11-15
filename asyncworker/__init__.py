from asyncworker.base import BaseApp
from asyncworker.consumer import Consumer
from asyncworker.options import Options, Defaultvalues, Events
from asyncworker.signal_handlers.amqp import AMQP
from asyncworker.signal_handlers.http_server import HTTPServer


class App(BaseApp):
    handlers = (HTTPServer(), AMQP())

    def __init__(self, host, user, password, prefetch_count):
        super(App, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.prefetch_count = prefetch_count

    def _build_consumers(self):
        consumers = []
        for route_info in self.routes_registry.amqp_routes:
            consumers.append(Consumer(route_info, self.host, self.user, self.password, self.prefetch_count))
        return consumers
