import asyncio
from typing import List

from aiohttp import web

from asyncworker import App, Options
from asyncworker.rabbitmq import RabbitMQMessage

try:
    from healthchecker import check
    from healthchecker.async_checker import AsyncCheckCase
    HEALTHCHECKER_ENABLED = True
except ImportError:
    HEALTHCHECKER_ENABLED = False


__doc__ = """
Run me with ASYNCWORKER_HTTP_ENABLED=1 python examples/with_http_server.py
Then access http://localhost:8080/ or http://localhost:8080/healthcheck (if you 
have "health-checker" package installed)
"""

app = App(host="localhost", user="guest", password="guest", prefetch_count=1024)


@app.route(routes=['/', '/a'], type='http', methods=['GET'])
async def index(request: web.Request) -> web.Response:
    return web.Response(body="Hello world")


if HEALTHCHECKER_ENABLED:
    @app.route(routes=['/healthcheck'], type='http', methods=['GET'])
    class HealthCheck(AsyncCheckCase, web.View):
        @property
        def loop(self) -> asyncio.AbstractEventLoop:
            return self.request.app.loop

        async def get(self) -> 'web.Response':
            """
            Should return 200 if all dependencies are ok, 500 otherwise.
            :returns: A HTTP response with True or False for each check
            """
            await self.check()

            status_code = 200 if self.has_succeeded() else 500

            return web.json_response(data=self.check_report, status=status_code)

        @check
        async def validate_something(self):
            return True

        @check
        async def validate_something_else(self):
            return False


@app.route(routes=["words_to_index"], type='amqp', vhost="/", options={Options.BULK_SIZE: 1})
async def drain_handler(messages: List[RabbitMQMessage]):
    print(messages)


app.run()
