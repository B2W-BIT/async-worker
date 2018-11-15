import asyncio
from typing import Iterable

from aiohttp import Signal

from asyncworker.conf import logger
from asyncworker.signal_handlers.http_server import HTTPServer
from asyncworker.models import RoutesRegistry, RouteTypes
from asyncworker.utils import entrypoint


class BaseApp:
    handlers = (HTTPServer(),)

    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.routes_registry = RoutesRegistry()
        self.consumers = []

        self._on_startup = Signal(self)
        self._on_shutdown = Signal(self)

        for handler in self.handlers:
            if handler.is_enabled:
                self._on_startup.append(handler.startup)
                self._on_shutdown.append(handler.shutdown)

    def _build_consumers(self):
        raise NotImplementedError()

    @entrypoint
    async def run(self):
        logger.info("Booting App...")
        self._on_startup.freeze()
        self._on_shutdown.freeze()
        await self.startup()

        while True:
            await asyncio.sleep(10)

    async def startup(self):
        """Causes on_startup signal

        Should be called in the event loop along with the request handler.
        """
        await self._on_startup.send(self)

    def route(self,
              routes: Iterable[str],
              type: str=RouteTypes.AMQP,
              options: dict=None,
              **kwargs):
        if options is None:
            options = {}
        if isinstance(type, RouteTypes):
            route_type = type
        else:
            route_type = RouteTypes[type.upper()]

        def wrapper(f):
            self.routes_registry[f] = {
                'type': route_type,
                'routes': routes,
                'handler': f,
                'options': options,
                **kwargs
            }
            return f
        return wrapper
