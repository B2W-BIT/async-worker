import asynctest

from asyncworker import App
from asyncworker.conf import settings
from asyncworker.connections import AMQPConnection
from asyncworker.options import (
    Options,
    DefaultValues,
    Events,
    Actions,
    RouteTypes,
)
from asyncworker.rabbitmq import AMQPRouteOptions
from asyncworker.routes import AMQPRoute


class RabbitMQAppTest(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.connection = AMQPConnection(
            hostname="127.0.0.1",
            username="guest",
            password="guest",
            prefetch=1024,
        )
        self.app = App(connections=[self.connection])

    async def tearDown(self):
        await self.app.shutdown()

    async def test_check_route_registry_full_options(self):
        expected_routes = ["/asgard/counts/ok"]
        expected_vhost = "/"

        @self.app.amqp.consume(
            expected_routes,
            vhost=expected_vhost,
            options=AMQPRouteOptions(bulk_size=1024, bulk_flush_interval=120),
        )
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        expected_registry_entry = AMQPRoute(
            type=RouteTypes.AMQP_RABBITMQ,
            routes=expected_routes,
            handler=_handler,
            default_options={},
            vhost=expected_vhost,
            options={
                "bulk_size": 1024,
                "bulk_flush_interval": 120,
                Events.ON_SUCCESS: Actions.ACK,
                Events.ON_EXCEPTION: Actions.REQUEUE,
            },
        )
        route = self.app.routes_registry.route_for(_handler)
        self.assertEqual(expected_registry_entry, route)
        self.assertEqual(42, await route["handler"](None))

    async def test_register_hander_on_route_registry(self):
        @self.app.amqp.consume(["/asgard/counts/ok"])
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        route = self.app.routes_registry.amqp_routes[0]
        self.assertEqual(_handler, route["handler"])
        self.assertEqual(42, await route["handler"](None))

    async def test_register_list_of_routes_to_the_same_handler(self):
        expected_routes = ["/asgard/counts/ok", "/asgard/counts/errors"]

        @self.app.amqp.consume(expected_routes)
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        route = self.app.routes_registry.amqp_routes[0]
        self.assertEqual(expected_routes, route["routes"])
        self.assertEqual(42, await route["handler"](None))

    async def test_register_with_default_vhost(self):
        expected_route = ["/asgard/counts/ok"]
        expected_vhost = settings.AMQP_DEFAULT_VHOST

        @self.app.amqp.consume(expected_route)
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        route = self.app.routes_registry.amqp_routes[0]
        self.assertEqual(expected_vhost, route["vhost"])
        self.assertEqual(42, await route["handler"](None))

    async def test_register_bulk_size(self):
        expected_bulk_size = 1024

        @self.app.amqp.consume(
            ["my-queue"], options=AMQPRouteOptions(bulk_size=expected_bulk_size)
        )
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        route = self.app.routes_registry.amqp_routes[0]
        self.assertEqual(expected_bulk_size, route["options"]["bulk_size"])
        self.assertEqual(42, await route["handler"](None))

    async def test_register_bulk_flush_timeout(self):
        expected_bulk_flush_interval = 120

        @self.app.amqp.consume(
            ["my-queue"],
            options=AMQPRouteOptions(
                bulk_flush_interval=expected_bulk_flush_interval
            ),
        )
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        route = self.app.routes_registry.amqp_routes[0]
        self.assertEqual(
            expected_bulk_flush_interval,
            route["options"]["bulk_flush_interval"],
        )
        self.assertEqual(42, await route["handler"](None))

    async def test_register_default_bulk_size_and_default_bulk_flush_timeout(
        self
    ):
        @self.app.amqp.consume(["my-queue"])
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        route = self.app.routes_registry.amqp_routes[0]
        self.assertEqual(DefaultValues.BULK_SIZE, route["options"]["bulk_size"])
        self.assertEqual(
            DefaultValues.BULK_FLUSH_INTERVAL,
            route["options"]["bulk_flush_interval"],
        )
        self.assertEqual(42, await route["handler"](None))

    async def test_register_action_on_success(self):
        @self.app.amqp.consume(
            ["my-queue"], options=AMQPRouteOptions(on_success=Actions.REJECT)
        )
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        self.assertEqual(
            Actions.REJECT,
            self.app.routes_registry[_handler]["options"][Events.ON_SUCCESS],
        )

    async def test_register_action_on_exception(self):
        @self.app.amqp.consume(
            ["my-queue"], options=AMQPRouteOptions(on_exception=Actions.ACK)
        )
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        self.assertEqual(
            Actions.ACK,
            self.app.routes_registry[_handler]["options"][Events.ON_EXCEPTION],
        )

    async def test_test_register_default_actions(self):
        @self.app.amqp.consume(["my-queue"])
        async def _handler(message):
            return 42

        self.assertIsNotNone(self.app.routes_registry)
        route = self.app.routes_registry.amqp_routes[0]
        self.assertEqual(Actions.ACK, route["options"][Events.ON_SUCCESS])
        self.assertEqual(Actions.REQUEUE, route["options"][Events.ON_EXCEPTION])

    async def test_app_receives_queue_connection(self):
        self.assertCountEqual(self.app.connections.values(), [self.connection])

    async def test_instantiate_one_consumer_per_handler_one_handler_registered(
        self
    ):
        """
        Para cada handler registrado, teremos um Consumer. Esse Consumer conseguirá consumir múltiplas
        filas, se necessário.
        """

        @self.app.amqp.consume(["asgard/counts"], vhost="/")
        async def _handler(message):
            return message

        await self.app.startup()
        consumers = self.app[RouteTypes.AMQP_RABBITMQ]["consumers"]
        self.assertEqual(1, len(consumers))
        self.assertEqual(["asgard/counts"], consumers[0].queue_name)
        self.assertEqual("/", consumers[0].vhost)

        queue_connection_parameters = consumers[
            0
        ].queue.connection.connection_parameters
        self.assertEqual(
            self.connection.hostname, queue_connection_parameters["host"]
        )
        self.assertEqual(
            self.connection.username, queue_connection_parameters["login"]
        )
        self.assertEqual(
            self.connection.password, queue_connection_parameters["password"]
        )
        self.assertEqual(
            self.connection.prefetch, consumers[0].queue.prefetch_count
        )

    async def test_instantiate_one_consumer_per_handler_multiple_handlers_registered_bla(
        self
    ):
        @self.app.amqp.consume(["asgard/counts"], vhost="/")
        async def _handler(message):
            return message

        @self.app.amqp.consume(["asgard/counts/errors"], vhost="fluentd")
        async def _other_handler(message):
            return message

        await self.app.startup()
        consumers = self.app[RouteTypes.AMQP_RABBITMQ]["consumers"]
        self.assertEqual(2, len(consumers))

        self.assertEqual(["asgard/counts"], consumers[0].queue_name)
        self.assertEqual("/", consumers[0].vhost)
        queue_connection_parameters = consumers[
            0
        ].queue.connection.connection_parameters
        self.assertEqual(
            self.connection.hostname, queue_connection_parameters["host"]
        )
        self.assertEqual(
            self.connection.username, queue_connection_parameters["login"]
        )
        self.assertEqual(
            self.connection.password, queue_connection_parameters["password"]
        )
        self.assertEqual(
            self.connection.prefetch, consumers[0].queue.prefetch_count
        )

        self.assertEqual(["asgard/counts/errors"], consumers[1].queue_name)
        self.assertEqual("fluentd", consumers[1].vhost)
        queue_connection_parameters = consumers[
            1
        ].queue.connection.connection_parameters
        self.assertEqual(
            self.connection.hostname, queue_connection_parameters["host"]
        )
        self.assertEqual(
            self.connection.username, queue_connection_parameters["login"]
        )
        self.assertEqual(
            self.connection.password, queue_connection_parameters["password"]
        )
        self.assertEqual(
            self.connection.prefetch, consumers[1].queue.prefetch_count
        )
