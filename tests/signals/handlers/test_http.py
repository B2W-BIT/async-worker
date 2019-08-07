import asyncio
import os
from random import randint

import asynctest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
from asynctest import mock, CoroutineMock, Mock, patch

from asyncworker import App
from asyncworker.conf import settings, Settings
from asyncworker.routes import RouteTypes, RoutesRegistry, call_http_handler
from asyncworker.signals.handlers.http import HTTPServer
from asyncworker.types.registry import TypesRegistry


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

        self.assertIsInstance(self.app[RouteTypes.HTTP]["app"], web.Application)
        self.assertIsInstance(
            self.app[RouteTypes.HTTP]["runner"], web.AppRunner
        )
        self.assertIsInstance(self.app[RouteTypes.HTTP]["site"], web.TCPSite)

        self.assertEqual(
            len(self.app[RouteTypes.HTTP]["app"]._router.routes()), 3
        )

        self.assertEqual(
            self.app[RouteTypes.HTTP]["site"]._port, settings.HTTP_PORT
        )
        self.assertEqual(
            self.app[RouteTypes.HTTP]["site"]._host, settings.HTTP_HOST
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

        self.assertEqual(self.app, {})

        await self.signal_handler.shutdown(self.app)

        cleanup.assert_not_awaited()

    async def test_simple_handler_200_response(self):
        """
        Tests if a response is correctly handled, Starts a real aiohttp server
        """

        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        async def index(r):
            return web.json_response({"OK": True})

        with mock.patch.dict(os.environ, ASYNCWORKER_HTTP_PORT="9999"):
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                await self.signal_handler.startup(self.app)
                async with TestClient(
                    TestServer(self.app[RouteTypes.HTTP]["app"]),
                    loop=asyncio.get_event_loop(),
                ) as client:
                    resp = await client.get("/")
                    self.assertEqual(resp.status, 200)
                    data = await resp.json()
                    self.assertDictEqual({"OK": True}, data)
                await self.signal_handler.shutdown(self.app)

    async def test_can_call_handler_without_annotation(self):
        """
        For backward compatiilty, wew can call a handler that receives
        one parameter and does not have any type annotations
        """

        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        async def handler(request):
            return web.json_response({})

        with mock.patch.dict(os.environ, ASYNCWORKER_HTTP_PORT="9999"):
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                await self.signal_handler.startup(self.app)
                async with TestClient(
                    TestServer(self.app[RouteTypes.HTTP]["app"]),
                    loop=asyncio.get_event_loop(),
                ) as client:
                    resp = await client.get("/")
                    self.assertEqual(200, resp.status)
                await self.signal_handler.shutdown(self.app)

    async def test_add_registry_to_all_requests(self):
        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        async def handler(request: web.Request):
            registry: TypesRegistry = request["types_registry"]
            assert registry is not None
            assert isinstance(registry, TypesRegistry)
            return web.json_response({})

        with mock.patch.dict(os.environ, ASYNCWORKER_HTTP_PORT="9999"):
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                await self.signal_handler.startup(self.app)
                async with TestClient(
                    TestServer(self.app[RouteTypes.HTTP]["app"]),
                    loop=asyncio.get_event_loop(),
                ) as client:
                    resp = await client.get("/")
                    self.assertEqual(200, resp.status)
                await self.signal_handler.shutdown(self.app)

    async def test_resolves_handler_parameters(self):
        expected_user_name = "Some User Name"

        class User:
            def __init__(self, name):
                self.name = name

        def insert_user_into_type_registry(handler):
            async def _wrapper(request: web.Request):
                request["types_registry"].set(User(name=expected_user_name))
                return await call_http_handler(request, handler)

            return _wrapper

        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        @insert_user_into_type_registry
        async def handler(user: User):
            return web.json_response({"name": user.name})

        with mock.patch.dict(os.environ, ASYNCWORKER_HTTP_PORT="9999"):
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                await self.signal_handler.startup(self.app)
                async with TestClient(
                    TestServer(self.app[RouteTypes.HTTP]["app"]),
                    loop=asyncio.get_event_loop(),
                ) as client:
                    resp = await client.get("/")
                    self.assertEqual(200, resp.status)
                    resp_data = await resp.json()
                    self.assertEqual({"name": expected_user_name}, resp_data)
                await self.signal_handler.shutdown(self.app)

    async def test_multiple_decorators_using_call_handler(self):
        expected_user_name = "Some User Name"
        expected_account_name = "Account Name"

        class User:
            def __init__(self, name):
                self.name = name

        class Account:
            def __init__(self, name):
                self.name = name

        def insert_user_into_type_registry(handler):
            async def _wrapper(request: web.Request):
                request["types_registry"].set(User(name=expected_user_name))
                return await call_http_handler(request, handler)

            return _wrapper

        def insert_account_into_type_registry(handler):
            async def _wrapper(request: web.Request):
                request["types_registry"].set(
                    Account(name=expected_account_name)
                )
                return await call_http_handler(request, handler)

            return _wrapper

        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        @insert_account_into_type_registry
        @insert_user_into_type_registry
        async def handler(user: User, account: Account):
            return web.json_response(
                {"account": account.name, "user": user.name}
            )

        with mock.patch.dict(os.environ, ASYNCWORKER_HTTP_PORT="9999"):
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                await self.signal_handler.startup(self.app)
                async with TestClient(
                    TestServer(self.app[RouteTypes.HTTP]["app"]),
                    loop=asyncio.get_event_loop(),
                ) as client:
                    resp = await client.get("/")
                    self.assertEqual(200, resp.status)
                    resp_data = await resp.json()
                    self.assertEqual(
                        {
                            "user": expected_user_name,
                            "account": expected_account_name,
                        },
                        resp_data,
                    )
                await self.signal_handler.shutdown(self.app)

    async def test_resolves_handler_parameters_when_receiving_request(self):
        def my_decorator(handler):
            async def _wrapper(request: web.Request):
                return await call_http_handler(request, handler)

            return _wrapper

        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        @my_decorator
        async def handler(request: web.Request):
            return web.json_response({"num": request.query["num"]})

        with mock.patch.dict(os.environ, ASYNCWORKER_HTTP_PORT="9999"):
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                await self.signal_handler.startup(self.app)
                async with TestClient(
                    TestServer(self.app[RouteTypes.HTTP]["app"]),
                    loop=asyncio.get_event_loop(),
                ) as client:
                    resp = await client.get("/", params={"num": 42})
                    self.assertEqual(200, resp.status)
                    resp_data = await resp.json()
                    self.assertEqual({"num": "42"}, resp_data)
                await self.signal_handler.shutdown(self.app)
