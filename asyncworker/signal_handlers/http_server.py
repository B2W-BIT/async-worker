from aiohttp import web
from typing import TYPE_CHECKING

from asyncworker.signal_handlers.base import SignalHandler

if TYPE_CHECKING:  # pragma: no cover
    from asyncworker.base import BaseApp

from asyncworker.conf import settings


class HTTPServer(SignalHandler):
    is_enabled = settings.HTTP_ENABLED

    async def startup(self, app: 'BaseApp'):
        app.http_app = web.Application()
        for route in app.routes_registry.http_routes:
            app.http_app.router.add_route(**route)

        app.http_runner = web.AppRunner(app.http_app)
        await app.http_runner.setup()
        site = web.TCPSite(runner=app.http_runner,
                           host=settings.HTTP_HOST,
                           port=settings.HTTP_PORT)
        await site.start()

    async def shutdown(self, app: 'BaseApp'):
        await app.http_runner.cleanup()
