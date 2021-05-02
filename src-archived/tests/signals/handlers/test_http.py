import os
from http import HTTPStatus
from importlib import reload
from random import randint

import asynctest
from aiohttp import web
from aiohttp.client import ClientSession
from asynctest import mock, CoroutineMock, Mock, patch

from asyncworker import App, conf
from asyncworker.conf import settings, Settings
from asyncworker.http.wrapper import RequestWrapper
from asyncworker.routes import call_http_handler, RouteTypes, RoutesRegistry
from asyncworker.signals.handlers.http import HTTPServer
from asyncworker.testing import HttpClientContext
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
        self.app = App(connections=[])

    async def tearDown(self):
        await self.app.shutdown()

    @asynctest.patch("asyncworker.signals.handlers.http.web.TCPSite.start")
    async def test_startup_initializes_an_web_application(self, start):
        self.app.routes_registry = self.routes_registry

        await self.signal_handler.startup(self.app)

        self.assertIsInstance(self.app[RouteTypes.HTTP]["app"], web.Application)
        self.assertIsInstance(
            self.app[RouteTypes.HTTP]["runner"], web.AppRunner
        )
        site: web.TCPSite = self.app[RouteTypes.HTTP]["site"]
        self.assertIsInstance(site, web.TCPSite)

        self.assertEqual(site._port, settings.HTTP_PORT)
        self.assertEqual(site._host, settings.HTTP_HOST)

        start.assert_awaited_once()

    @asynctest.patch("asyncworker.signals.handlers.http.web.AppRunner.cleanup")
    async def test_add_handler_for_metrics_endpoint(self, cleanup):
        await self.signal_handler.startup(self.app)

        async with ClientSession() as client:
            async with client.get(
                f"http://{settings.HTTP_HOST}:{settings.HTTP_PORT}{settings.METRICS_ROUTE_PATH}"
            ) as resp:
                self.assertEqual(200, resp.status)

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

        self.assertNotIn("runner", self.app[RouteTypes.HTTP])

        await self.signal_handler.shutdown(self.app)

        cleanup.assert_not_awaited()

    async def test_simple_handler_200_response(self):
        """
        Tests if a response is correctly handled, Starts a real aiohttp server
        """

        @self.app.http.get(["/"])
        async def index():
            return web.json_response({"OK": True})

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                resp = await client.get("/")
                self.assertEqual(resp.status, 200)
                data = await resp.json()
                self.assertDictEqual({"OK": True}, data)

    async def test_user_can_use_metrics_endpoint_if_default_is_renamed(self):
        """
        Se estivermos com o endpoint de métricas habilitado mas o path foi trocado
        então devemos poder registrar um endpoint com o valor default do path de metricas

        Não é o melhor jeito de fazer o teste mas como o settings é instanciado no nível do módulo
        não temos muito com controlar o desencadear dos imports então por isso preciso ficar substiuindo
        os módulos para que o "novo" settings (após reload()) surta efeito.
        """
        from asyncworker import routes

        app = App()

        with mock.patch.dict(
            os.environ, ASYNCWORKER_METRICS_ROUTE_PATH="/asyncworker-metrics"
        ):

            reload(conf)
            with mock.patch.object(routes, "conf", conf):

                @app.http.get(["/metrics"])
                async def _h():
                    return web.json_response({})

                async with HttpClientContext(app) as client:
                    resp = await client.get("/metrics")
                    self.assertEqual(HTTPStatus.OK, resp.status)

    async def test_user_can_use_metrics_if_method_is_not_get(self):
        """
        Deve ser possível usar o endpoint de métricas se o method for diferente de GET.
        """
        from asyncworker import routes

        app = App()

        @app.http.post([settings.METRICS_ROUTE_PATH])
        async def _h():
            return web.json_response({"OK": True})

        async with HttpClientContext(app) as client:
            resp = await client.post(settings.METRICS_ROUTE_PATH)
            self.assertEqual(HTTPStatus.OK, resp.status)

            self.assertEqual({"OK": True}, await resp.json())

    async def test_can_call_handler_without_annotation(self):
        """
        For backward compatiilty, wew can call a handler that receives
        one parameter and does not have any type annotations
        """

        @self.app.http.get(["/"])
        async def handler():
            return web.json_response({"OK": True})

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                resp = await client.get("/")
                self.assertEqual(200, resp.status)
                self.assertEqual({"OK": True}, await resp.json())

    async def test_add_registry_to_all_requests(self):
        @self.app.http.get(["/"])
        async def handler(wrapper: RequestWrapper):
            request = wrapper.http_request
            registry: TypesRegistry = request["types_registry"]
            assert registry is not None
            assert isinstance(registry, TypesRegistry)
            return web.json_response({})

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                resp = await client.get("/")
                self.assertEqual(200, resp.status)

    async def test_resolves_handler_parameters(self):
        expected_user_name = "Some User Name"

        class User:
            def __init__(self, name):
                self.name = name

        def insert_user_into_type_registry(handler):
            async def _wrapper(wrapper: RequestWrapper):
                wrapper.types_registry.set(User(name=expected_user_name))
                return await call_http_handler(wrapper, handler)

            return _wrapper

        @self.app.http.get(["/"])
        @insert_user_into_type_registry
        async def handler(user: User):
            return web.json_response({"name": user.name})

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                resp = await client.get("/")
                self.assertEqual(200, resp.status)
                resp_data = await resp.json()
                self.assertEqual({"name": expected_user_name}, resp_data)

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
            async def _wrapper(wrapper: RequestWrapper):
                wrapper.types_registry.set(User(name=expected_user_name))
                return await call_http_handler(wrapper, handler)

            return _wrapper

        def insert_account_into_type_registry(handler):
            async def _wrapper(wrapper: RequestWrapper):
                wrapper.types_registry.set(Account(name=expected_account_name))
                return await call_http_handler(wrapper, handler)

            return _wrapper

        @self.app.http.get(["/"])
        @insert_account_into_type_registry
        @insert_user_into_type_registry
        async def handler(user: User, account: Account):
            return web.json_response(
                {"account": account.name, "user": user.name}
            )

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
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

    async def test_resolves_handler_parameters_when_receiving_request_wrapper(
        self
    ):
        def my_decorator(handler):
            async def _wrapper(wrapper: RequestWrapper):
                return await call_http_handler(wrapper, handler)

            return _wrapper

        @self.app.http.get(["/"])
        @my_decorator
        async def handler(wrapper: RequestWrapper):
            return web.json_response({"num": wrapper.http_request.query["num"]})

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                resp = await client.get("/", params={"num": 42})
                self.assertEqual(200, resp.status)
                resp_data = await resp.json()
                self.assertEqual({"num": "42"}, resp_data)

    async def test_ignores_return_annotation_when_resolving_parameters(self):
        @self.app.http.get(["/"])
        async def handler(wrapper: RequestWrapper) -> web.Response:
            return web.json_response({"num": wrapper.http_request.query["num"]})

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                resp = await client.get("/", params={"num": 42})
                self.assertEqual(200, resp.status)
                resp_data = await resp.json()
                self.assertEqual({"num": "42"}, resp_data)

    async def test_handler_can_receive_aiohttp_request(self):
        @self.app.http.get(["/"])
        async def handler(request: web.Request) -> web.Response:
            return web.json_response({"num": request.query["num"]})

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                resp = await client.get("/", params={"num": 42})
                self.assertEqual(200, resp.status)
                resp_data = await resp.json()
                self.assertEqual({"num": "42"}, resp_data)

    async def test_handler_decorator_can_receive_aiohttp_request(self):
        def my_decorator(handler):
            async def _wrapper(request: web.Request):
                r_wrapper = RequestWrapper(
                    http_request=request,
                    types_registry=request["types_registry"],
                )
                return await call_http_handler(r_wrapper, handler)

            return _wrapper

        @self.app.http.get(["/"])
        @my_decorator
        async def handler(wrapper: RequestWrapper):
            return web.json_response({"num": wrapper.http_request.query["num"]})

        async with HttpClientContext(self.app) as client:
            settings_mock = Settings()
            with mock.patch(
                "asyncworker.signals.handlers.http.settings", settings_mock
            ):
                resp = await client.get("/", params={"num": 42})
                self.assertEqual(200, resp.status)
                resp_data = await resp.json()
                self.assertEqual({"num": "42"}, resp_data)
