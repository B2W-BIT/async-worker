import functools
import asyncio

from .consumer import Consumer

from asyncworker import conf
from asyncworker.options import Options, Defaultvalues, Events
from .bucket import Bucket

def entrypoint(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))
    return _


class App:
    def __init__(self, host, user, password, prefetch_count):
        self.routes_registry = {}
        self.host = host
        self.user = user
        self.password = password
        self.prefetch_count = prefetch_count

    def route(self, routes, vhost="/", options={}):
        def wrap(f):
            self.routes_registry[f] = {
                "route": routes,
                "handler": f,
                "options": {
                    "vhost": vhost,
                    "bulk_size": options.get(Options.BULK_SIZE, Defaultvalues.BULK_SIZE),
                    "bulk_flush_interval": options.get(Options.BULK_FLUSH_INTERVAL, Defaultvalues.BULK_FLUSH_INTERVAL),
                    Events.ON_SUCCESS: options.get(Events.ON_SUCCESS, Defaultvalues.ON_SUCCESS),
                    Events.ON_EXCEPTION: options.get(Events.ON_EXCEPTION, Defaultvalues.ON_EXCEPTION),
                }
            }
            return f
        return wrap

    def _build_consumers(self):
        consumers = []
        for _handler, route_info in self.routes_registry.items():
            consumers.append(Consumer(route_info, self.host, self.user, self.password, self.prefetch_count))
        return consumers

    @entrypoint
    async def run(self):
        conf.logger.info("Booting App...")
        consumers = self._build_consumers()
        for consumer in consumers:
            asyncio.get_event_loop().create_task(consumer.start())
        while True:
            await asyncio.sleep(10)

