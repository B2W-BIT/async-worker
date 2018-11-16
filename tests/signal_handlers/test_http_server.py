import asynctest
from aiohttp import web
from asynctest import CoroutineMock, Mock

from asyncworker import BaseApp
from asyncworker.conf import settings
from asyncworker.signal_handlers.http_server import HTTPServer
from asyncworker.models import RouteTypes, RoutesRegistry


class AMQPTests(asynctest.TestCase):
    async def setUp(self):
        self.signal_handler = HTTPServer()

        handler1 = Mock(return_value=CoroutineMock())
        handler2 = Mock(return_value=CoroutineMock())

        self.routes_registry = RoutesRegistry(
            {
                handler1: {
                    "type": RouteTypes.HTTP,
                    "routes": ["/xablau"],
                    "methods": ['GET']
                },
                handler2: {
                    "type": RouteTypes.HTTP,
                    "routes": ["/xena"],
                    "methods": ['GET', 'POST']
                },
            }
        )

    @asynctest.patch("asyncworker.signal_handlers.http_server.web.TCPSite.start")
    async def test_startup_initializes_an_web_application(self, start):
        app = BaseApp()
        app.routes_registry = self.routes_registry

        await self.signal_handler.startup(app)

        self.assertIsInstance(app['http_app'], web.Application)
        self.assertIsInstance(app['http_runner'], web.AppRunner)
        self.assertIsInstance(app['http_site'], web.TCPSite)

        self.assertEqual(len(app['http_app']._router.routes()), 3)

        self.assertEqual(app['http_site']._port, settings.HTTP_PORT)
        self.assertEqual(app['http_site']._host, settings.HTTP_HOST)

        start.assert_awaited_once()

    @asynctest.patch("asyncworker.signal_handlers.http_server.web.AppRunner.cleanup")
    async def test_shutdown_closes_the_running_http_server(self, cleanup):
        app = BaseApp()
        app.routes_registry = self.routes_registry

        await self.signal_handler.startup(app)
        cleanup.assert_not_awaited()

        await self.signal_handler.shutdown(app)
        cleanup.assert_awaited_once()
