from collections.abc import ValuesView
from typing import ItemsView

import asynctest
from asynctest import Mock

from asyncworker.conf import settings
from asyncworker.connections import AMQPConnection
from asyncworker.easyqueue.queue import JsonQueue


class AMQPConnectionTests(asynctest.TestCase):
    async def setUp(self):
        self.username = "admin"
        self.password = "123456"
        self.hostname = "127.0.0.1"
        self.rabbitmq_connection = AMQPConnection(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
        )

        self.body = asynctest.Mock()
        self.routing_key = asynctest.Mock()
        self.exchange = asynctest.Mock()

    async def tearDown(self):
        asynctest.patch.stopall()

    def test_len_returns_the_number_of_registered_connections(self):
        self.assertEqual(len(self.rabbitmq_connection), 0)

        self.rabbitmq_connection.register(asynctest.Mock())

        self.assertEqual(len(self.rabbitmq_connection), 1)

    def test_rabbitmq_connection_is_iterable(self):
        connection_a = asynctest.Mock(virtual_host="a", spec=JsonQueue)
        connection_b = asynctest.Mock(virtual_host="b", spec=JsonQueue)

        self.rabbitmq_connection.register(connection_a)
        self.rabbitmq_connection.register(connection_b)

        as_dict = dict(self.rabbitmq_connection)
        self.assertEqual(as_dict, {"a": connection_a, "b": connection_b})

    def test_register_registers_a_new_unique_connection_for_a_given_vhost(self):
        connection_a = asynctest.Mock(virtual_host="a", spec=JsonQueue)
        connection_b = asynctest.Mock(virtual_host="b", spec=JsonQueue)

        self.rabbitmq_connection.register(connection_a)
        self.rabbitmq_connection.register(connection_b)

        self.assertEqual(self.rabbitmq_connection["a"], connection_a)
        self.assertEqual(self.rabbitmq_connection["b"], connection_b)

    async def test_put_uses_the_right_connection_for_a_given_vhost(self):
        connection_a = asynctest.Mock(virtual_host="a", spec=JsonQueue)
        connection_b = asynctest.Mock(virtual_host="b", spec=JsonQueue)

        self.rabbitmq_connection.register(connection_a)
        self.rabbitmq_connection.register(connection_b)

        await self.rabbitmq_connection.put(
            serialized_data=self.body,
            routing_key=self.routing_key,
            exchange=self.exchange,
            vhost="a",
        )

        connection_b.put.assert_not_awaited()
        connection_a.put.assert_awaited_once_with(
            data=None,
            routing_key=self.routing_key,
            exchange=self.exchange,
            serialized_data=self.body,
            immediate=False,
            mandatory=False,
            properties=None,
        )

    async def test_put_uses_the_default_vhost_if_none_is_provided(self):
        connection_a = asynctest.Mock(
            virtual_host=settings.AMQP_DEFAULT_VHOST, spec=JsonQueue
        )
        connection_b = asynctest.Mock(virtual_host="b", spec=JsonQueue)

        self.rabbitmq_connection.register(connection_a)
        self.rabbitmq_connection.register(connection_b)

        await self.rabbitmq_connection.put(
            data=self.body, routing_key=self.routing_key, exchange=self.exchange
        )

        connection_b.put.assert_not_awaited()
        connection_a.put.assert_awaited_once_with(
            data=self.body,
            routing_key=self.routing_key,
            exchange=self.exchange,
            serialized_data=None,
            immediate=False,
            mandatory=False,
            properties=None,
        )

    async def test_put_initializes_a_new_connection_if_a_connection_wasnt_initialized_for_a_given_vhost(
        self
    ):
        connection_a = asynctest.Mock(virtual_host="a", spec=JsonQueue)

        with asynctest.patch(
            "asyncworker.connections.JsonQueue", return_value=connection_a
        ):
            await self.rabbitmq_connection.put(
                data=self.body,
                routing_key=self.routing_key,
                exchange=self.exchange,
                vhost="a",
            )

            connection_a.put.assert_awaited_once_with(
                data=self.body,
                routing_key=self.routing_key,
                exchange=self.exchange,
                serialized_data=None,
                immediate=False,
                mandatory=False,
                properties=None,
            )

    async def test_initialize_with_connections(self):
        connection_a = asynctest.Mock(
            virtual_host=settings.AMQP_DEFAULT_VHOST, spec=JsonQueue
        )
        connection_b = asynctest.Mock(virtual_host="b", spec=JsonQueue)
        conn = AMQPConnection(
            hostname="localhost",
            username="guest",
            password="pwd",
            connections={"a": connection_a, "b": connection_b},
        )
        self.assertEqual(
            {"a": connection_a, "b": connection_b}, conn.connections
        )

    async def test_items(self):
        conn = AMQPConnection(
            hostname="localhost", username="guest", password="pwd"
        )
        self.assertEqual(ItemsView(conn), conn.items())

    async def test_values(self):
        self.maxDiff = None
        conn = AMQPConnection(
            hostname="localhost", username="guest", password="pwd"
        )
        self.assertEqual(str(ValuesView(conn)), str(conn.values()))
