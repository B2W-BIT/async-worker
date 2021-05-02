import asyncio
from http import HTTPStatus
from signal import Signals

import asynctest
from aiohttp import web
from asynctest import Mock, CoroutineMock, patch, call

from asyncworker.app import App
from asyncworker.connections import AMQPConnection
from asyncworker.exceptions import InvalidConnection
from asyncworker.http import HTTPMethods
from asyncworker.options import RouteTypes, DefaultValues, Options
from asyncworker.routes import AMQPRoute
from asyncworker.task_runners import ScheduledTaskRunner
from asyncworker.testing import HttpClientContext


class AppTests(asynctest.TestCase):
    async def setUp(self):
        class MyApp(App):
            handlers = (
                Mock(startup=CoroutineMock(), shutdown=CoroutineMock()),
            )

        self.appCls = MyApp
        self.app = MyApp(connections=[])

    async def test_setitem_changes_internal_state_if_not_frozen(self):
        self.app["foo"] = foo = asynctest.Mock()
        self.assertEqual(foo, self.app._state["foo"])

        await self.app.freeze()

        with self.assertRaises(RuntimeError):
            self.app["foo"] = "will raise an error"

    async def test_delitem_changes_internal_state_if_not_frozen(self):
        self.app["foo"] = "value"
        self.app["bar"] = "another value"

        del self.app["foo"]

        await self.app.freeze()

        with self.assertRaises(RuntimeError):
            del self.app["bar"]

    async def test_getitem_returns_internal_state_value(self):
        self.app["dog"] = "Xablau"

        self.assertEqual(self.app["dog"], "Xablau")

    async def test_len_returns_internal_state_len_value(self):
        self.app.update(pet="dog", name="Xablau")

        self.assertEqual(len(self.app), len(dict(self.app)))

    async def test_iter_iters_through_internal_state_value(self):
        self.app.update(pet="dog", name="Xablau")

        state = dict(**self.app)
        self.assertDictContainsSubset({"pet": "dog", "name": "Xablau"}, state)

    async def test_startup_freezes_applications_and_sends_the_on_startup_signal(
        self,
    ):
        await self.app.startup()

        self.assertTrue(self.app.frozen)
        # _on_startup.send.assert_awaited_once_with(self.app)

    async def test_route_raises_an_error_is_type_isnt_a_valid_RouteType(self):
        with self.assertRaises(TypeError):
            self.app.route(["route"], type="invalid")

    async def test_route_registers_a_route_to_routes_registry(self):
        async def handler(request):
            pass

        self.app.route(["route"], type=RouteTypes.AMQP_RABBITMQ, dog="Xablau")(
            handler
        )

        self.assertEqual(len(self.app.routes_registry), 1)
        self.assertIsInstance(self.app.routes_registry[handler], AMQPRoute)

    async def test_run_on_startup_registers_a_coroutine_to_be_executed_on_startup(
        self,
    ):
        coro = CoroutineMock()

        self.app.run_on_startup(coro)

        self.assertEqual(coro, self.app._on_startup[-1])

        await self.app.startup()
        coro.assert_awaited_once_with(self.app)

    async def test_startup_calls_user_registered_startup_routines_after_app_signal_handlers_startup(
        self,
    ):
        coro = CoroutineMock()

        self.app.run_on_startup(coro)

        self.assertEqual(
            self.app._on_startup,
            [*(handler.startup for handler in self.app.handlers), coro],
        )

    async def test_run_on_shutdown_registers_a_coroutine_to_be_executed_on_shutdown(
        self,
    ):
        coro = CoroutineMock()

        self.app.run_on_shutdown(coro)
        self.assertIn(coro, self.app._on_shutdown)

        await self.app.shutdown()
        coro.assert_awaited_once_with(self.app)

    async def test_shutdown_is_registered_as_a_signal_handler(self):
        with patch.object(
            self.loop, "add_signal_handler"
        ) as add_signal_handler:
            app = self.appCls()
            add_signal_handler.assert_has_calls(
                [
                    call(Signals.SIGINT, app.shutdown),
                    call(Signals.SIGTERM, app.shutdown),
                ]
            )

    async def test_shutdown_schedules_on_shutdown_signal_send(self):
        with patch.object(self.app._on_shutdown, "send") as send:
            send.assert_not_awaited()

            shutdown_coro = self.app.shutdown()

            self.assertIsInstance(shutdown_coro, asyncio.Task)
            self.assertFalse(shutdown_coro.done())

            send.assert_not_awaited()

            await shutdown_coro
            send.assert_awaited_once_with(self.app)
            self.assertTrue(shutdown_coro.done())

    async def test_run_every_registers_a_coroutine_to_be_executed_as_a_ScheduledTaskRunner(
        self,
    ):
        with patch(
            "asyncworker.app.ScheduledTaskRunner", spec=ScheduledTaskRunner
        ) as Runner:
            seconds = 10
            coro = Mock(start=CoroutineMock(), stop=CoroutineMock())

            self.app.run_every(seconds=seconds)(coro)

            Runner.assert_called_once_with(
                seconds=seconds,
                task=coro,
                app=self.app,
                max_concurrency=DefaultValues.RUN_EVERY_MAX_CONCURRENCY,
            )
            self.assertIn(Runner.return_value.start, self.app._on_startup)
            self.assertIn(Runner.return_value.stop, self.app._on_shutdown)
            self.assertIn(Runner.return_value, self.app["task_runners"])

    async def test_run_every_max_concurrency_can_be_overwritten_with_options(
        self,
    ):
        with patch(
            "asyncworker.app.ScheduledTaskRunner", spec=ScheduledTaskRunner
        ) as Runner:
            seconds = 10
            coro = Mock(start=CoroutineMock(), stop=CoroutineMock())

            self.app.run_every(
                seconds=seconds, options={Options.MAX_CONCURRENCY: 666}
            )(coro)

            Runner.assert_called_once_with(
                seconds=seconds, task=coro, app=self.app, max_concurrency=666
            )

    async def test_http_route_decorator(self):

        app = App()

        @app.http._route(["/"], method=HTTPMethods.GET)
        async def _h():
            return web.json_response({})

        async with HttpClientContext(app) as client:
            resp = await client.get("/")
            self.assertEqual(200, resp.status)

            data = await resp.json()
            self.assertEqual({}, data)

    async def test_http_get_decorator(self):
        app = App()

        @app.http.get(["/"])
        async def _handler():
            return web.json_response({})

        async with HttpClientContext(app) as client:
            resp = await client.get("/")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({}, data)

    async def test_http_head_decorator(self):
        app = App()

        @app.http.head(["/"])
        async def _handler():
            return web.json_response({"OK": True})

        async with HttpClientContext(app) as client:
            resp = await client.head("/")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertIsNone(data)

    async def test_http_delete_decorator(self):
        app = App()

        @app.http.delete(["/"])
        async def _handler():
            return web.json_response({HTTPMethods.DELETE: True})

        async with HttpClientContext(app) as client:
            resp = await client.delete("/")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({HTTPMethods.DELETE: True}, data)

    async def test_http_patch_decorator(self):
        app = App()

        @app.http.patch(["/"])
        async def _handler():
            return web.json_response({HTTPMethods.PATCH: True})

        async with HttpClientContext(app) as client:
            resp = await client.patch("/", json={})
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({HTTPMethods.PATCH: True}, data)

    async def test_http_post_decorator(self):
        app = App()

        @app.http.post(["/"])
        async def _handler():
            return web.json_response({HTTPMethods.POST: True})

        async with HttpClientContext(app) as client:
            resp = await client.post("/", json={})
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({HTTPMethods.POST: True}, data)

    async def test_http_put_decorator(self):
        app = App()

        @app.http.put(["/"])
        async def _handler():
            return web.json_response({HTTPMethods.PUT: True})

        async with HttpClientContext(app) as client:
            resp = await client.put("/", json={})
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({HTTPMethods.PUT: True}, data)


class AppConnectionsTests(asynctest.TestCase):
    def setUp(self):
        super(AppConnectionsTests, self).setUp()
        self.connections = [
            AMQPConnection(
                name="conn1",
                hostname="localhost",
                username="guest",
                password="guest",
            ),
            AMQPConnection(
                name="conn2",
                hostname="localhost",
                username="guest",
                password="guest",
            ),
            AMQPConnection(
                hostname="localhost", username="guest", password="guest"
            ),
        ]

    def test_connections_gets_registered_into_a_connection_mapping(self):
        app = App(connections=self.connections)
        self.assertCountEqual(app.connections.values(), self.connections)

    def test_get_connection_returns_the_proper_connection(self):
        app = App(connections=self.connections)

        self.assertEqual(
            app.get_connection(name=self.connections[0].name),
            self.connections[0],
        )

    def test_get_connection_raises_an_error_if_theres_no_connection_registered_for_name(
        self,
    ):
        app = App(connections=self.connections)

        with self.assertRaises(InvalidConnection):
            app.get_connection(name="Unregistered connection name")
