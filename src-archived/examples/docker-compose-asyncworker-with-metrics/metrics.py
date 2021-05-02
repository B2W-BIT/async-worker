import asyncio
from dataclasses import dataclass
from urllib.parse import urljoin

from aiohttp import ClientSession, web
from aiologger import Logger

from asyncworker import App
from asyncworker.http.decorators import parse_path
from asyncworker.http.wrapper import RequestWrapper
from asyncworker.metrics import Counter, Gauge

app = App()
logger = Logger.with_default_handlers()

a_counter = Counter("a_counter", "A counter metric example")
request_couter = Counter(
    "request_counter", "Performed requests counter", labelnames=["url"]
)
g = Gauge("duration", "Duration")
g_label = Gauge("with_label", "Gauge with label", labelnames=["label"])


@dataclass
class Request:
    path: str
    number_of_requests: int
    method: str = "GET"

    @property
    def url(self):
        return urljoin("http://asyncworker", self.path)


REQUESTS = [
    Request(path="/count", number_of_requests=1000),
    Request(path="/metrics", number_of_requests=1000),
    Request(path="/gauge-with-label/A", number_of_requests=1000),
    Request(path="/gauge-with-label/B", number_of_requests=1000),
    Request(path="/sleep/1", number_of_requests=10),
    Request(path="/sleep/5", number_of_requests=10),
    Request(path="/not_an_app_route", number_of_requests=10),
    Request(path="/not_an_app_route/1/2/3", number_of_requests=10),
    Request(path="/not_an_app_route", method="POST", number_of_requests=10),
    Request(path="/not_an_app_route", method="DELETE", number_of_requests=10),
]
REQUESTS_INTERVAL_IN_SECONDS = 15


@app.http.get(["/count"])
async def handler():
    a_counter.inc()
    return web.json_response({})


@app.http.get(["/sleep/{duration}"])
@parse_path
async def by_id(duration: int):
    with g.time():
        await asyncio.sleep(duration)
    return web.json_response({})


@app.http.get(["/gauge-with-label/{label}"])
@parse_path
async def one_param(label: str):
    with g_label.labels(label=label).track_inprogress():
        pass
    return web.json_response({})


@app.run_on_startup
async def startup(app):
    app["client_session"] = ClientSession()
    await logger.info("app started")


@app.run_on_shutdown
async def shutdown(app):
    await app["client_session"].close()
    await logger.info("app shutdown")


@app.run_every(seconds=REQUESTS_INTERVAL_IN_SECONDS)
async def make_requests(app):
    session: ClientSession = app["client_session"]

    async def perform_request(request: Request):
        async with session.request(
            method=request.method, url=request.url
        ) as response:
            await response.read()
            request_couter.labels(url=request.url).inc()

    await logger.info("Generating requests.")

    for request in REQUESTS:
        for _ in range(request.number_of_requests):
            asyncio.create_task(perform_request(request))


app.run()
