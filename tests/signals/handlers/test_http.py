from random import randint

import asynctest
from aiohttp import web
from asynctest import CoroutineMock, Mock, patch

from asyncworker import App
from asyncworker.conf import settings
from asyncworker.signals.handlers.http import HTTPServer
from asyncworker.routes import RouteTypes, RoutesRegistry


class HTTPServerTests(asynctest.TestCase):
    async def setUp(self):
        self.signal_handler = HTTPServer()

        handler1 = Mock(return_value=CoroutineMock())
        handler2 = Mock(return_value=CoroutineMock())

        self.routes_registry = RoutesRegistry(
            {
                handler1: {
                    "type": RouteTypes.HTTP,
                    "routes": ["/xablau"],
                    "methods": ["GET"],
                },
                handler2: {
                    "type": RouteTypes.HTTP,
                    "routes": ["/xena"],
                    "methods": ["GET", "POST"],
                },
            }
        )
        self.app = App("localhost", "guest", "guest", 1)

    @asynctest.patch("asyncworker.signals.handlers.http.web.TCPSite.start")
    async def test_startup_initializes_an_web_application(self, start):
        self.app.routes_registry = self.routes_registry

        await self.signal_handler.startup(self.app)

        self.assertIsInstance(
            self.app[RouteTypes.HTTP]["http_app"], web.Application
        )
        self.assertIsInstance(
            self.app[RouteTypes.HTTP]["http_runner"], web.AppRunner
        )
        self.assertIsInstance(
            self.app[RouteTypes.HTTP]["http_site"], web.TCPSite
        )

        self.assertEqual(
            len(self.app[RouteTypes.HTTP]["http_app"]._router.routes()), 3
        )

        self.assertEqual(
            self.app[RouteTypes.HTTP]["http_site"]._port, settings.HTTP_PORT
        )
        self.assertEqual(
            self.app[RouteTypes.HTTP]["http_site"]._host, settings.HTTP_HOST
        )

        start.assert_awaited_once()

    @asynctest.patch("asyncworker.signals.handlers.http.web.TCPSite.start")
    async def test_startup_doesnt_initializes_an_web_application_if_there_are_no_http_routes(
        self, start
    ):
        await self.signal_handler.startup(self.app)

        start.assert_not_awaited()
        self.assertNotIn("http_app", self.app[RouteTypes.HTTP])
        self.assertNotIn("http_runner", self.app[RouteTypes.HTTP])
        self.assertNotIn("http_site", self.app[RouteTypes.HTTP])

    @asynctest.patch("asyncworker.signals.handlers.http.web.AppRunner.cleanup")
    async def test_shutdown_closes_the_running_http_server(self, cleanup):
        with patch(
            "asyncworker.signals.handlers.http.settings",
            HTTP_PORT=randint(30000, 60000),
        ):
            self.app.routes_registry = self.routes_registry

        await self.signal_handler.startup(self.app)
        cleanup.assert_not_awaited()

        await self.signal_handler.shutdown(self.app)
        cleanup.assert_awaited_once()

    @asynctest.patch("asyncworker.signals.handlers.http.web.AppRunner.cleanup")
    async def test_shutdown_does_nothing_if_app_doesnt_have_an_http_runner(
        self, cleanup
    ):
        self.app.routes_registry = self.routes_registry

        self.assertNotIn("http_runner", self.app[RouteTypes.HTTP])

        await self.signal_handler.shutdown(self.app)

        cleanup.assert_not_awaited()
