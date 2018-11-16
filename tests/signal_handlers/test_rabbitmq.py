import asynctest
from asynctest import CoroutineMock, Mock, call

from asyncworker.signal_handlers.rabbitmq import RabbitMQ, Consumer
from asyncworker.models import RouteTypes, RoutesRegistry


class AMQPTests(asynctest.TestCase):
    async def setUp(self):
        self.signal_handler = RabbitMQ()

        handler1 = Mock(return_value=CoroutineMock())
        handler2 = Mock(return_value=CoroutineMock())

        self.routes_registry = RoutesRegistry(
            {
                handler1: {
                    "type": RouteTypes.AMQP,
                    "routes": ["Xablau"],
                    "options": {}
                },
                handler2: {
                    "type": RouteTypes.AMQP,
                    "routes": ["Xena"],
                    "options": {}
                },
            }
        )

    @asynctest.patch("asyncworker.signal_handlers.rabbitmq.Consumer.start")
    async def test_startup_initializes_and_starts_one_consumer_per_route(self,
                                                                         start):
        app = Mock(
            routes_registry=self.routes_registry,
            consumers=[],
            loop=Mock(create_task=CoroutineMock()),
            prefetch_count=1
        )
        await self.signal_handler.startup(app)

        self.assertEqual(len(app.consumers), 2)
        for consumer in app.consumers:
            self.assertIsInstance(consumer, Consumer)

        start.assert_has_calls([call(), call()])
