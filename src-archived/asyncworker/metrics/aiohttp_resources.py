from http import HTTPStatus
from typing import Callable, Awaitable

from aiohttp import web
from aiohttp.web_middlewares import middleware
from prometheus_client import generate_latest

from asyncworker import metrics
from asyncworker.metrics.registry import REGISTRY
from asyncworker.time import perf_counter_ms as now

_Handler = Callable[[web.Request], Awaitable[web.Response]]


def route_path_for_request(request: web.Request) -> str:
    if request.match_info.route.resource:
        return request.match_info.route.resource.canonical
    return "unregistered_path"


@middleware
async def http_metrics_middleware(request: web.Request, handler: _Handler):
    start = now()
    route_path = route_path_for_request(request)

    try:
        metrics.requests_in_progress.labels(
            method=request.method, path=route_path
        ).inc()
        response = await handler(request)
        metrics.response_size.labels(
            method=request.method, path=route_path
        ).observe(response.content_length)
        metrics.request_duration.labels(
            method=request.method, path=route_path, status=response.status
        ).observe(now() - start)

        return response
    except web.HTTPException as e:
        metrics.request_duration.labels(
            method=request.method, path=route_path, status=e.status
        ).observe(now() - start)
        metrics.response_size.labels(
            method=request.method, path=route_path
        ).observe(e.content_length)
        raise e
    except Exception as e:
        metrics.request_duration.labels(
            method=request.method,
            path=route_path,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        ).observe(now() - start)
        raise e
    finally:
        metrics.requests_in_progress.labels(
            method=request.method, path=route_path
        ).dec()


async def metrics_route_handler(request: web.Request) -> web.Response:
    response = web.Response(
        body=generate_latest(registry=REGISTRY), content_type="text/plain"
    )
    return response
