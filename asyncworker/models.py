from collections import UserDict
from enum import Enum, auto
from typing import Callable, Coroutine, Dict, List, Any

from cached_property import cached_property

from asyncworker.conf import settings
from asyncworker.options import Defaultvalues, Events, Options


RouteHandler = Callable[[], Coroutine]
Route = Dict[str, Any]


class _AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):  # type: ignore
        return name


class RouteTypes(str, Enum):
    AMQP = auto()
    HTTP = auto()


class RoutesRegistry(UserDict):
    @cached_property
    def http_routes(self) -> List[Route]:
        routes = []
        for handler, route in self.items():
            if route['type'] is not RouteTypes.HTTP:
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
            if route['type'] is not RouteTypes.AMQP:
                continue
            options = route['options']
            routes.append({
                "routes": route['routes'],
                "handler": handler,
                "options": {
                    "vhost": route.get('vhost',
                                       settings.AMQP_DEFAULT_VHOST),
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
