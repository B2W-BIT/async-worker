from typing import Callable, Awaitable

from aiohttp import web
from aiohttp.web_middlewares import middleware

from asyncworker import metrics
from asyncworker.conf import default_timer
from asyncworker.metrics.registry import generate_latest

_Handler = Callable[[web.Request], Awaitable[web.Response]]


@middleware
async def http_metrics_middleware(request: web.Request, handler: _Handler):
    start = default_timer()
    try:
        response = await handler(request)

        metrics.request_duration.labels(
            method=request.method, path=request.path, status=response.status
        ).observe(default_timer() - start)

        return response
    except web.HTTPException as e:
        metrics.request_duration.labels(
            method=request.method, path=request.path, status=e.status
        ).observe(default_timer() - start)
        raise e


async def metrics_route_handler(request: web.Request) -> web.Response:
    response = web.Response(body=generate_latest(), content_type="text/plain")
    return response
