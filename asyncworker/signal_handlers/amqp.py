from typing import TYPE_CHECKING

from asyncworker.consumer import Consumer
from asyncworker.signal_handlers.base import SignalHandler

if TYPE_CHECKING:
    from asyncworker import App


class AMQP(SignalHandler):
    async def startup(self, app: 'App'):
        for route_info in app.routes_registry.amqp_routes:
            consumer = Consumer(route_info, app.host, app.user,
                                app.password, app.prefetch_count)
            app.consumers.append(consumer)
            app.loop.create_task(consumer.start())
