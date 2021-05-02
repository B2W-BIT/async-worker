import asynctest
from asynctest import CoroutineMock, Mock, call, patch, ANY

from asyncworker import App
from asyncworker.connections import AMQPConnection
from asyncworker.consumer import Consumer
from asyncworker.exceptions import InvalidRoute, InvalidConnection
from asyncworker.options import RouteTypes
from asyncworker.routes import RoutesRegistry
from asyncworker.signals.handlers.rabbitmq import RabbitMQ


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
        connection = AMQPConnection(
            hostname="127.0.0.1",
            username="guest",
            password="guest",
            prefetch=1024,
        )
        app = App(connections=[connection])
        app.routes_registry = self.routes_registry
        app.loop = Mock(create_task=CoroutineMock())
        # asynctest.MagicMock(
        #     routes_registry=,
        #     loop=Mock(create_task=CoroutineMock()),
        # )

        app[RouteTypes.AMQP_RABBITMQ] = {"connections": [connection]}
        await self.signal_handler.startup(app)

        Consumer.assert_has_calls(
            [
                call(
                    route_info=self.routes_registry.amqp_routes[0],
                    host=connection.hostname,
                    username=connection.username,
                    password=connection.password,
                    prefetch_count=connection.prefetch,
                ),
                call(
                    route_info=self.routes_registry.amqp_routes[1],
                    host=connection.hostname,
                    username=connection.username,
                    password=connection.password,
                    prefetch_count=connection.prefetch,
                ),
            ],
            any_order=True,
        )
        Consumer.return_value.start.assert_has_calls([call(), call()])
        self.assertEqual(
            app[RouteTypes.AMQP_RABBITMQ]["consumers"],
            [Consumer.return_value, Consumer.return_value],
        )

    @asynctest.patch(
        "asyncworker.signals.handlers.rabbitmq.AMQPConnection.register"
    )
    async def test_startup_registers_one_connection_per_vhost_into_app_state(
        self, register
    ):
        conn = AMQPConnection(
            hostname="127.0.0.1",
            username="guest",
            password="guest",
            prefetch=1024,
        )
        app = App(connections=[conn])
        app.routes_registry = self.routes_registry
        await self.signal_handler.startup(app)

        self.assertIn(conn, app.connections)
        register.assert_has_calls(
            [
                call(consumer.queue)
                for consumer in app[RouteTypes.AMQP_RABBITMQ]["consumers"]
            ]
        )

    async def test_it_raises_an_error_if_theres_multiple_connections_and_route_doesnt_define_a_connection(
        self
    ):
        conn1 = AMQPConnection(
            hostname="127.0.0.1",
            username="guest",
            password="guest",
            prefetch=1024,
        )
        conn2 = AMQPConnection(
            hostname="127.0.0.1",
            username="guest",
            password="guest",
            prefetch=1024,
        )
        app = App(connections=[conn1, conn2])

        @app.amqp.consume(routes=["a_queue_name"])
        async def mock_handler(*args, **kwargs):
            pass

        with self.assertRaises(InvalidRoute):
            await self.signal_handler.startup(app)

    async def test_it_raises_an_error_if_an_amqp_route_is_registered_without_any_defined_connections(
        self
    ):
        app = App(connections=[])

        @app.amqp.consume(routes=["a_queue_name"])
        async def mock_handler(*args, **kwargs):
            pass

        with self.assertRaises(InvalidRoute):
            await self.signal_handler.startup(app)

    async def test_it_uses_the_connection_provided_by_the_route_if_one_exists(
        self
    ):
        conn = AMQPConnection(
            hostname="127.0.0.1",
            username="guest",
            password="guest",
            prefetch=1024,
        )
        app = App(connections=[])

        @app.route(
            routes=["a_queue_name"],
            type=RouteTypes.AMQP_RABBITMQ,
            options={"connection": conn},
        )
        async def mock_handler(*args, **kwargs):
            pass

        MockedConsumer = Mock(return_value=Mock(spec=Consumer, queue=Mock()))
        with patch(
            "asyncworker.signals.handlers.rabbitmq.Consumer", MockedConsumer
        ):
            await self.signal_handler.startup(app)

        MockedConsumer.assert_called_once_with(
            route_info=ANY,
            host=conn.hostname,
            username=conn.username,
            password=conn.password,
            prefetch_count=conn.prefetch,
        )

    async def test_it_uses_the_connection_name_provided_by_the_route_if_one_exists(
        self
    ):
        app = App(connections=[])

        @app.route(
            routes=["a_queue_name"],
            type=RouteTypes.AMQP_RABBITMQ,
            options={"connection": "XablauConnection"},
        )
        async def mock_handler(*args, **kwargs):
            pass

        MockedConsumer = Mock(return_value=Mock(spec=Consumer, queue=Mock()))
        with patch(
            "asyncworker.signals.handlers.rabbitmq.Consumer", MockedConsumer
        ):
            with self.assertRaises(InvalidConnection):
                await self.signal_handler.startup(app)
