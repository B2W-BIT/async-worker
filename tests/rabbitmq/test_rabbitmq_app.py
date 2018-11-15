import asynctest

from asyncworker import App
from asyncworker.conf import settings
from asyncworker.options import Options, Defaultvalues, Events, Actions


class RabbitMQAppTest(asynctest.TestCase):
    def setUp(self):
        self.connection_parameters = {
            "host": "127.0.0.1",
            "user": "guest",
            "password": "guest",
            "prefetch_count": 1024
        }

    async def test_check_route_registry_full_options(self):
        expected_routes = ["/asgard/counts/ok"]
        expected_vhost = "/"
        app = App(**self.connection_parameters)

        @app.route(expected_routes,
                   vhost=expected_vhost,
                   options={
                       Options.BULK_SIZE: 1024,
                       Options.BULK_FLUSH_INTERVAL: 120
                   })
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        expected_registry_entry = {
            "routes": expected_routes,
            "handler": _handler,
            "options": {
                "vhost": expected_vhost,
                "bulk_size": 1024,
                "bulk_flush_interval": 120,
                Events.ON_SUCCESS: Actions.ACK,
                Events.ON_EXCEPTION: Actions.REQUEUE,
            }
        }
        route = app.routes_registry.amqp_routes[0]
        self.assertEqual(expected_registry_entry, route)
        self.assertEqual(42, await route['handler'](None))

    async def test_register_hander_on_route_registry(self):
        app = App(**self.connection_parameters)

        @app.route(["/asgard/counts/ok"])
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        route = app.routes_registry.amqp_routes[0]
        self.assertEqual(_handler, route['handler'])
        self.assertEqual(42, await route['handler'](None))

    async def test_register_list_of_routes_to_the_same_handler(self):
        expected_routes = ["/asgard/counts/ok", "/asgard/counts/errors"]
        app = App(**self.connection_parameters)

        @app.route(expected_routes)
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        route = app.routes_registry.amqp_routes[0]
        self.assertEqual(expected_routes, route['routes'])
        self.assertEqual(42, await route['handler'](None))

    async def test_register_with_default_vhost(self):
        expected_route = ["/asgard/counts/ok"]
        expected_vhost = settings.AMQP_DEFAULT_VHOST
        app = App(**self.connection_parameters)

        @app.route(expected_route)
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        route = app.routes_registry.amqp_routes[0]
        self.assertEqual(expected_vhost, route['options']['vhost'])
        self.assertEqual(42, await route['handler'](None))


    async def test_register_bulk_size(self):
        expected_bulk_size = 1024
        app = App(**self.connection_parameters)

        @app.route(["my-queue"], options={Options.BULK_SIZE: expected_bulk_size})
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        route = app.routes_registry.amqp_routes[0]
        self.assertEqual(expected_bulk_size, route['options']['bulk_size'])
        self.assertEqual(42, await route['handler'](None))

    async def test_register_bulk_flush_timeout(self):
        expected_bulk_flush_interval = 120
        app = App(**self.connection_parameters)

        @app.route(["my-queue"], options={Options.BULK_FLUSH_INTERVAL: expected_bulk_flush_interval})
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        route = app.routes_registry.amqp_routes[0]
        self.assertEqual(expected_bulk_flush_interval, route['options']['bulk_flush_interval'])
        self.assertEqual(42, await route['handler'](None))

    async def test_register_default_bulk_size_and_default_bulk_flush_timeout(self):
        app = App(**self.connection_parameters)

        @app.route(["my-queue"])
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        route = app.routes_registry.amqp_routes[0]
        self.assertEqual(Defaultvalues.BULK_SIZE, route['options']['bulk_size'])
        self.assertEqual(Defaultvalues.BULK_FLUSH_INTERVAL, route['options']['bulk_flush_interval'])
        self.assertEqual(42, await route['handler'](None))

    async def test_register_action_on_success(self):
        app = App(**self.connection_parameters)

        @app.route(["my-queue"], options = {Events.ON_SUCCESS: Actions.REJECT})
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        self.assertEqual(Actions.REJECT, app.routes_registry[_handler]['options'][Events.ON_SUCCESS])

    async def test_register_action_on_exception(self):
        app = App(**self.connection_parameters)

        @app.route(["my-queue"], options = {Events.ON_EXCEPTION: Actions.ACK})
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        self.assertEqual(Actions.ACK, app.routes_registry[_handler]['options'][Events.ON_EXCEPTION])

    async def test_test_register_default_actions(self):
        app = App(**self.connection_parameters)

        @app.route(["my-queue"])
        async def _handler(message):
            return 42

        self.assertIsNotNone(app.routes_registry)
        route = app.routes_registry.amqp_routes[0]
        self.assertEqual(Actions.ACK, route['options'][Events.ON_SUCCESS])
        self.assertEqual(Actions.REQUEUE, route['options'][Events.ON_EXCEPTION])

    async def test_app_receives_queue_connection(self):
        app = App(host="127.0.0.1", user="guest", password="guest", prefetch_count=1024)
        self.assertEqual("127.0.0.1", app.host)
        self.assertEqual("guest", app.user)
        self.assertEqual("guest", app.password)
        self.assertEqual(1024, app.prefetch_count)

    async def test_instantiate_one_consumer_per_handler_one_handler_registered(self):
        """
        Para cada handler registrado, teremos um Consumer. Esse Consumer conseguirá consumir múltiplas
        filas, se necessário.
        """
        app = App(**self.connection_parameters)

        @app.route(["asgard/counts"], vhost="/")
        async def _handler(message):
            return message

        consumers = app._build_consumers()
        self.assertEqual(1, len(consumers))
        self.assertEqual(["asgard/counts"], consumers[0].queue_name)
        self.assertEqual("/", consumers[0].vhost)

        queue_connection_parameters = consumers[0].queue.connection_parameters
        self.assertEqual(self.connection_parameters['host'], queue_connection_parameters['host'])
        self.assertEqual(self.connection_parameters['user'], queue_connection_parameters['login'])
        self.assertEqual(self.connection_parameters['password'], queue_connection_parameters['password'])
        self.assertEqual(self.connection_parameters['prefetch_count'], consumers[0].queue.prefetch_count)

    async def test_instantiate_one_consumer_per_handler_multiple_handlers_registered(self):
        app = App(**self.connection_parameters)

        @app.route(["asgard/counts"], vhost="/")
        async def _handler(message):
            return message

        @app.route(["asgard/counts/errors"], vhost="fluentd")
        async def _other_handler(message):
            return message

        consumers = app._build_consumers()
        self.assertEqual(2, len(consumers))

        self.assertEqual(["asgard/counts"], consumers[0].queue_name)
        self.assertEqual("/", consumers[0].vhost)
        queue_connection_parameters = consumers[0].queue.connection_parameters
        self.assertEqual(self.connection_parameters['host'], queue_connection_parameters['host'])
        self.assertEqual(self.connection_parameters['user'], queue_connection_parameters['login'])
        self.assertEqual(self.connection_parameters['password'], queue_connection_parameters['password'])
        self.assertEqual(self.connection_parameters['prefetch_count'], consumers[0].queue.prefetch_count)

        self.assertEqual(["asgard/counts/errors"], consumers[1].queue_name)
        self.assertEqual("fluentd", consumers[1].vhost)
        queue_connection_parameters = consumers[1].queue.connection_parameters
        self.assertEqual(self.connection_parameters['host'], queue_connection_parameters['host'])
        self.assertEqual(self.connection_parameters['user'], queue_connection_parameters['login'])
        self.assertEqual(self.connection_parameters['password'], queue_connection_parameters['password'])
        self.assertEqual(self.connection_parameters['prefetch_count'], consumers[1].queue.prefetch_count)
