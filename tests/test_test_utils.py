import asyncio
import os

from aiohttp import web
from aiohttp.test_utils import TestClient
from asynctest import TestCase, mock
from asyncworker import App, RouteTypes
from asyncworker.testing import http_client, HttpClientContext


class HttpClientTestCaseDecoratorTest(TestCase):
    async def setUp(self):
        self.app = App("", "", "", 1)

    async def test_client_is_passed_to_test(self):
        @http_client(self.app)
        async def my_test_case(client):
            return client

        client = await my_test_case()
        self.assertTrue(isinstance(client, TestClient))

    async def test_client_can_perform_http_requests(self):
        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        async def index(request):
            return web.json_response({"OK": True})

        @http_client(self.app)
        async def my_method(http_client):
            resp = await http_client.get("/")
            data = await resp.json()
            return data

        returned_data = await my_method()

        self.assertEqual({"OK": True}, returned_data)

    async def test_decorated_method_can_have_its_own_params(self):
        @http_client(self.app)
        async def my_method(http_client, a, b):
            return (http_client, a, b)

        rv = await my_method(42, 10)

        self.assertTrue(isinstance(rv[0], TestClient))
        self.assertEqual([42, 10], [rv[1], rv[2]])

    async def test_server_is_closed_if_handler_raises_exception(self):
        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        async def index(request):
            return web.json_response({"OK": True})

        with mock.patch.dict(os.environ, TEST_ASYNCWORKER_HTTP_PORT="9999"):

            @http_client(self.app)
            async def my_method(http_client):
                raise Exception("BOOM")

            with self.assertRaises(Exception):
                await my_method()

            @http_client(self.app)
            async def other_method(http_client):
                resp = await http_client.get("/")
                return await resp.json()

            self.assertEqual({"OK": True}, await other_method())


class HttpClientContextManagerTest(TestCase):
    async def setUp(self):
        self.app = App("", "", "", 1)

    async def test_client_can_perform_requests(self):
        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        async def index(request):
            return web.json_response({"OK": True})

        async with HttpClientContext(self.app) as http_client:
            resp = await http_client.get("/")
            self.assertEqual({"OK": True}, await resp.json())

    async def test_can_reuse_port(self):
        @self.app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
        async def index(request):
            return web.json_response({"OK": True})

        with mock.patch.dict(os.environ, TEST_ASYNCWORKER_HTTP_PORT="9999"):
            async with HttpClientContext(self.app) as http_client:
                resp = await http_client.get("/")
                self.assertEqual({"OK": True}, await resp.json())

            async with HttpClientContext(self.app) as http_client:
                resp = await http_client.get("/")
                self.assertEqual({"OK": True}, await resp.json())
