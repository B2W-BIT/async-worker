import os
from functools import wraps
from typing import Tuple

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from asyncworker import App


async def _get_client_and_server(app: App) -> Tuple[TestClient, TestServer]:
    routes = app.routes_registry.http_routes
    http_app = web.Application()

    for route in routes:
        for route_def in route.aiohttp_routes():
            route_def.register(http_app.router)

    port = int(os.getenv("TEST_ASYNCWORKER_HTTP_PORT") or 0)
    server = TestServer(http_app, port=port)
    client = TestClient(server)
    await server.start_server()
    return (client, server)


def http_client(app: App):
    def decorator(handler, *args, **kwargs):
        @wraps(handler)
        async def inner_deco(*args, **kwargs):
            client, server = await _get_client_and_server(app)

            try:
                return await handler(*args, client, **kwargs)
            except Exception as e:
                raise e
            finally:
                await server.close()
                await client.close()

        return inner_deco

    return decorator


class HttpClientContext:
    def __init__(self, app: App) -> None:
        self.app = app

    async def __aenter__(self) -> TestClient:
        self.client, self.server = await _get_client_and_server(self.app)
        return self.client

    async def __aexit__(self, *args, **kwargs):
        await self.server.close()
        await self.client.close()
