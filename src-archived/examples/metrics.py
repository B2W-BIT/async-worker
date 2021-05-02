import asyncio

from aiohttp import web

from asyncworker import App, RouteTypes
from asyncworker.http.decorators import parse_path
from asyncworker.http.wrapper import RequestWrapper
from asyncworker.metrics import Counter, Gauge

app = App()


c = Counter("count", "Contagem")
g = Gauge("duration", "Duration")

g_label = Gauge("with_label", "Gauge with label", labelnames=["label"])


@app.run_on_startup
async def startup(app):
    print("app started")


@app.route(["/count"], type=RouteTypes.HTTP, methods=["GET"])
async def handler():
    c.inc()
    return web.json_response({})


@app.route(["/sleep/{duration}"], type=RouteTypes.HTTP, methods=["GET"])
@parse_path
async def by_id(duration: int):
    with g.time():
        await asyncio.sleep(duration)
    return web.json_response({})


@app.route(["/gauge-with-label/{label}"], type=RouteTypes.HTTP, methods=["GET"])
@parse_path
async def one_param(label: str):
    with g_label.labels(label=label).track_inprogress():
        pass
    return web.json_response({})


app.run()
