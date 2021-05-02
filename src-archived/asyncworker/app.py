import asyncio
from collections.abc import MutableMapping
from signal import Signals
from typing import Iterable, Callable, Coroutine, Dict, Any, Optional

from asyncworker.conf import logger
from asyncworker.connections import ConnectionsMapping, Connection
from asyncworker.exceptions import InvalidRoute, InvalidConnection
from asyncworker.http.entrypoints import HTTPEntryPointImpl
from asyncworker.options import RouteTypes, Options, DefaultValues
from asyncworker.rabbitmq.entrypoints import AMQPRouteEntryPointImpl
from asyncworker.routes import RoutesRegistry, Route
from asyncworker.signals.base import Signal, Freezable
from asyncworker.signals.handlers.http import HTTPServer
from asyncworker.signals.handlers.rabbitmq import RabbitMQ
from asyncworker.task_runners import ScheduledTaskRunner
from asyncworker.utils import entrypoint


class App(MutableMapping, Freezable):
    handlers = (RabbitMQ(), HTTPServer())
    shutdown_os_signals = (Signals.SIGINT, Signals.SIGTERM)

    def __init__(
        self, connections: Optional[Iterable[Connection]] = None
    ) -> None:
        Freezable.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.routes_registry = RoutesRegistry()
        self.default_route_options: dict = {}

        self._state: Dict[Any, Any] = self._get_initial_state()
        self.connections = ConnectionsMapping()
        if connections:
            self.connections.add(connections)

        self._on_startup: Signal = Signal(self)
        self._on_shutdown: Signal = Signal(self)

        for handler in self.handlers:
            self._on_startup.append(handler.startup)
            self._on_shutdown.append(handler.shutdown)

        for signal in self.shutdown_os_signals:
            self.loop.add_signal_handler(signal, self.shutdown)

    def _check_frozen(self):
        if self.frozen:
            raise RuntimeError(
                "You shouldn't change the state of a started application"
            )

    async def freeze(self):
        await self.connections.freeze()
        await super(App, self).freeze()

    def get_connection(self, name: str) -> Connection:
        try:
            return self.connections[name]
        except KeyError as e:
            raise InvalidConnection(
                f"There's no Connection with name `{name}` registered "
                f"in `App.connections`"
            ) from e

    def _get_initial_state(self) -> Dict[str, Dict]:
        # fixme: typeignore reason - https://github.com/python/mypy/issues/4537
        return {route_type: {} for route_type in RouteTypes}  # type: ignore

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

    @entrypoint
    async def run(self):
        await logger.debug({"event": "Booting App..."})
        await self.startup()

        await self._on_shutdown.wait()

    async def startup(self):
        """
        Causes on_startup signal

        Should be called in the event loop along with the request handler.
        """
        await self._on_startup.send(self)

    def shutdown(self) -> asyncio.Future:
        """
        Schedules an on_startup signal

        Is called automatically when the application receives
        a SIGINT or SIGTERM
        """
        return asyncio.ensure_future(self._on_shutdown.send(self))

    @property
    def http(self) -> HTTPEntryPointImpl:
        return HTTPEntryPointImpl(self)

    @property
    def amqp(self) -> AMQPRouteEntryPointImpl:
        return AMQPRouteEntryPointImpl(self)

    def route(
        self,
        routes: Iterable[str],
        type: RouteTypes,
        options: dict = None,
        **kwargs,
    ):
        if options is None:
            options = {}
        if not isinstance(type, RouteTypes):
            raise TypeError(
                f"type parameter is not a valid RouteTypes." f" Found: '{type}'"
            )

        def wrapper(f):
            handler = f
            if not asyncio.iscoroutinefunction(handler):
                try:
                    handler = f.__call__
                    if not asyncio.iscoroutinefunction(handler):
                        raise TypeError(
                            f"handler must be a coroutine: {handler}"
                        )
                except AttributeError:
                    raise TypeError(
                        f"Object passed as handler is not callable: {f}"
                    )

            self.routes_registry[handler] = {
                "type": type,
                "routes": routes,
                "handler": handler,
                "options": options,
                "default_options": self.default_route_options,
                **kwargs,
            }

            return f

        return wrapper

    def run_on_startup(self, coro: Callable[["App"], Coroutine]) -> None:
        """
        Registers a coroutine to be awaited for during app startup
        """
        self._on_startup.append(coro)

    def run_on_shutdown(self, coro: Callable[["App"], Coroutine]) -> None:
        """
        Registers a coroutine to be awaited for during app shutdown
        """
        self._on_shutdown.append(coro)

    def run_every(self, seconds: int, options: Dict = None):
        """
        Registers a coroutine to be called with a given interval
        """
        if options is None:
            options = {}

        max_concurrency = options.get(
            Options.MAX_CONCURRENCY, DefaultValues.RUN_EVERY_MAX_CONCURRENCY
        )

        def wrapper(task: Callable[..., Coroutine]):
            runner = ScheduledTaskRunner(
                seconds=seconds,
                task=task,
                app=self,
                max_concurrency=max_concurrency,
            )
            self._on_startup.append(runner.start)
            self._on_shutdown.append(runner.stop)
            if "task_runners" not in self:
                self["task_runners"] = []
            self["task_runners"].append(runner)

            return task

        return wrapper

    def get_connection_for_route(self, route_info: Route):
        route_connection = route_info.connection
        if route_connection is None:
            route_connection = route_info.options.get("connection")

        connections = self.connections.with_type(route_info.type)
        if route_connection is not None:
            if isinstance(route_connection, Connection):
                return route_connection
            elif isinstance(route_connection, str):
                return self.get_connection(name=route_connection)
            else:
                # pragma: nocover
                raise InvalidRoute(
                    f"Expected `Route.connection` to be either `str` or "
                    f"`Connection`. Got `{type(route_connection)}` instead."
                )
        elif len(connections) > 1:
            raise InvalidRoute(
                f"Invalid route definition for App. You are trying to "
                f"define a {route_info.type} into an asyncworker.App "
                f"with multiple connections without specifying which "
                f"one to use."
            )
        else:
            try:
                return connections[0]
            except IndexError as e:
                raise InvalidRoute(
                    f"Invalid route definition for App. You are trying to "
                    f"define a {route_info.type} without an "
                    f"Connection registered on App"
                ) from e
