import asyncio
import warnings
from collections import MutableMapping
from typing import Iterable

from aiohttp import Signal

from asyncworker.conf import logger
from asyncworker.signal_handlers.http_server import HTTPServer
from asyncworker.models import RoutesRegistry, RouteTypes
from asyncworker.utils import entrypoint


class BaseApp(MutableMapping):
    handlers = (HTTPServer(),)

    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.routes_registry = RoutesRegistry()
        self.consumers = []

        self._state = {}
        self._frozen = False
        self._on_startup = Signal(self)
        self._on_shutdown = Signal(self)

        for handler in self.handlers:
            if handler.is_enabled:
                self._on_startup.append(handler.startup)
                self._on_shutdown.append(handler.shutdown)

    def _check_frozen(self):
        if self._frozen:
            raise RuntimeError("You shouldnt change the state of started "
                               "application")

    @property
    def frozen(self) -> bool:
        return self._frozen

    def freeze(self) -> None:
        self._frozen = True

    def __getitem__(self, key):
        return self._state[key]

    def __setitem__(self, key, value):
        self._check_frozen()
        self._state[key] = value

    def __delitem__(self, key):
        self._check_frozen()
        del self._state[key]

    def __len__(self):
        return len(self._state)

    def __iter__(self):
        return iter(self._state)

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
