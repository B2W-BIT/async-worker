from aiohttp import web

from asyncworker.conf import settings
from asyncworker.metrics.aiohttp_resources import (
    http_metrics_middleware,
    metrics_route_handler,
)
from asyncworker.options import RouteTypes
from asyncworker.signals.handlers.base import SignalHandler


class HTTPServer(SignalHandler):
    async def startup(self, app):
        app[RouteTypes.HTTP] = {}
        routes = app.routes_registry.http_routes
        if not routes:
            return

        app[RouteTypes.HTTP]["app"] = http_app = web.Application(
            middlewares=(http_metrics_middleware,)
        )
        http_app.router.add_route(
            method="GET",
            path=settings.METRICS_ENDPOINT,
            handler=metrics_route_handler,
        )

        for route in routes:
            for route_def in route.aiohttp_routes():
                route_def.register(http_app.router)

        app[RouteTypes.HTTP]["runner"] = web.AppRunner(http_app)
        await app[RouteTypes.HTTP]["runner"].setup()
        app[RouteTypes.HTTP]["site"] = web.TCPSite(
            runner=app[RouteTypes.HTTP]["runner"],
            host=settings.HTTP_HOST,
            port=settings.HTTP_PORT,
        )
        await app[RouteTypes.HTTP]["site"].start()

    async def shutdown(self, app):
        if RouteTypes.HTTP in app and "runner" in app[RouteTypes.HTTP]:
            await app[RouteTypes.HTTP]["runner"].cleanup()
