import asynctest
from asynctest import CoroutineMock, Mock, call

from asyncworker import App
from asyncworker.rabbitmq.connection import AMQPConnection
from asyncworker.signals.handlers.rabbitmq import RabbitMQ
from asyncworker.routes import RoutesRegistry
from asyncworker.options import RouteTypes


class AMQPTests(asynctest.TestCase):
    async def setUp(self):
        self.signal_handler = RabbitMQ()

        handler1 = Mock(return_value=CoroutineMock())
        handler2 = Mock(return_value=CoroutineMock())

        self.routes_registry = RoutesRegistry(
            {
                handler1: {
                    "type": RouteTypes.AMQP_RABBITMQ,
                    "routes": ["Xablau"],
                    "options": {},
                },
                handler2: {
                    "type": RouteTypes.AMQP_RABBITMQ,
                    "routes": ["Xena"],
                    "options": {},
                    "vhost": "k9",
                },
            }
        )

    @asynctest.patch("asyncworker.signals.handlers.rabbitmq.Consumer")
    async def test_startup_initializes_and_starts_one_consumer_per_route(
        self, Consumer
    ):
        app = asynctest.MagicMock(
            routes_registry=self.routes_registry,
            loop=Mock(create_task=CoroutineMock()),
            prefetch_count=1,
        )
        await self.signal_handler.startup(app)

        Consumer.assert_has_calls(
            [
                call(
                    self.routes_registry.amqp_routes[0],
                    app.host,
                    app.user,
                    app.password,
                    app.prefetch_count,
                ),
                call(
                    self.routes_registry.amqp_routes[1],
                    app.host,
                    app.user,
                    app.password,
                    app.prefetch_count,
                ),
            ],
            any_order=True,
        )
        Consumer.return_value.start.assert_has_calls([call(), call()])
        app[
            RouteTypes.AMQP_RABBITMQ
        ].__getitem__.return_value.append.assert_has_calls(
            [call(Consumer.return_value), call(Consumer.return_value)]
        )

    @asynctest.patch(
        "asyncworker.signals.handlers.rabbitmq.AMQPConnection.register"
    )
    async def test_startup_registers_one_connection_per_vhost_into_app_state(
        self, register
    ):
        app = App(
            host="127.0.0.1",
            user="guest",
            password="guest",
            prefetch_count=1024,
        )
        app.routes_registry = self.routes_registry
        await self.signal_handler.startup(app)

        self.assertIsInstance(
            app[RouteTypes.AMQP_RABBITMQ]["connection"], AMQPConnection
        )
        register.assert_has_calls(
            [call(consumer.queue) for consumer in app["consumers"]]
        )
