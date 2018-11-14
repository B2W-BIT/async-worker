from collections import UserDict
from typing import Callable, Coroutine, Dict, List

from cached_property import cached_property

from asyncworker.options import Defaultvalues, Events, Options

Route = Callable[[], Coroutine]


class Routes(UserDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cache = {}

    @cached_property
    def http_routes(self) -> List[Dict]:
        routes = []
        for handler, route in self.items():
            if route['type'] != 'http':
                continue
            for path in route['routes']:
                for method in route['methods']:
                    routes.append({
                        'method': method,
                        'path': path,
                        'handler': handler
                    })
        return routes

    @cached_property
    def amqp_routes(self) -> List[Dict]:
        routes = []
        for handler, route in self.items():
            if route['type'] == 'amqp':
                options = route['options']
                routes.append({
                    "routes": route['routes'],
                    "handler": handler,
                    "options": {
                        "vhost": route['vhost'],
                        "bulk_size": options.get(Options.BULK_SIZE,
                                                 Defaultvalues.BULK_SIZE),
                        "bulk_flush_interval": options.get(
                            Options.BULK_FLUSH_INTERVAL,
                            Defaultvalues.BULK_FLUSH_INTERVAL),
                        Events.ON_SUCCESS: options.get(
                            Events.ON_SUCCESS,
                            Defaultvalues.ON_SUCCESS),
                        Events.ON_EXCEPTION: options.get(
                            Events.ON_EXCEPTION,
                            Defaultvalues.ON_EXCEPTION),
                    }
                })
        return routes
