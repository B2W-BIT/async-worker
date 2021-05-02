from typing import List, Optional

from asyncworker import conf
from asyncworker.connections import AMQPConnection
from asyncworker.entrypoints import EntrypointInterface, _extract_async_callable
from asyncworker.routes import AMQPRouteOptions, RoutesRegistry, AMQPRoute


def _register_amqp_handler(
    registry: RoutesRegistry,
    routes: List[str],
    vhost: str,
    connection: Optional[AMQPConnection],
    options: Optional[AMQPRouteOptions],
):
    def _wrap(f):

        cb = _extract_async_callable(f)
        route = AMQPRoute(
            handler=cb,
            routes=routes,
            vhost=vhost,
            connection=connection,
            options=options,
        )
        registry.add_amqp_route(route)

        return f

    return _wrap


class AMQPRouteEntryPointImpl(EntrypointInterface):
    def consume(
        self,
        routes: List[str],
        vhost: str = conf.settings.AMQP_DEFAULT_VHOST,
        connection: Optional[AMQPConnection] = None,
        options: Optional[AMQPRouteOptions] = AMQPRouteOptions(),
    ):
        return _register_amqp_handler(
            self.app.routes_registry, routes, vhost, connection, options
        )
