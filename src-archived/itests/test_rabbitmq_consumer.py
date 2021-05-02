import asyncio

from asynctest import TestCase

from asyncworker import App, RouteTypes
from asyncworker.connections import AMQPConnection

consume_callback_shoud_not_be_called = False
handler_with_requeue_called = 0
handler_without_requeue_called = 0
successful_message_value_is_equal = False

message_processed_multiple_connections = False
message_processed_other_vhost = False


class RabbitMQConsumerTest(TestCase):
    async def setUp(self):
        self.queue_name = "test"
        self.connection = AMQPConnection(
            hostname="127.0.0.1", username="guest", password="guest", prefetch=1
        )
        self.app = App(connections=[self.connection])

    async def tearDown(self):
        await self.app.connections.with_type(RouteTypes.AMQP_RABBITMQ)[0][
            "/"
        ].connection.channel.queue_delete(self.queue_name)
        handler_without_requeue_called = 0
        handler_with_requeue_called = 0

    async def test_process_one_successful_message(self):
        """
        Um worker com dois handlers um que publica e outro que lê a mensagem
        No final um ack() é chamado
        """
        message = {"key": "value"}

        @self.app.amqp.consume([self.queue_name])
        async def handler(messages):
            global successful_message_value_is_equal
            successful_message_value_is_equal = (
                messages[0].body["key"] == message["key"]
            )

        await self.app.startup()
        queue = self.connection["/"]
        await queue.connection._connect()
        await queue.connection.channel.queue_declare(self.queue_name)

        await queue.put(routing_key=self.queue_name, data=message)
        await asyncio.sleep(1)
        self.assertTrue(successful_message_value_is_equal)
        await self.app.shutdown()

    async def test_process_message_reject_with_requeue(self):
        """
        Causamos um erro no handler para que a mensagem seja rejeitada e
        recolocada na fila.
        O handler confirmará a mensagem na segunda tentativa (`msg.ack()`)
        """

        @self.app.amqp.consume([self.queue_name])
        async def other_handler(messages):
            global handler_with_requeue_called
            if handler_with_requeue_called > 0:
                messages[0].accept()
            else:
                handler_with_requeue_called += 1
            value = messages[0].field  # AttributeError

        await self.app.startup()
        queue = self.connection["/"]
        await queue.connection._connect()
        await queue.connection.channel.queue_declare(self.queue_name)

        await queue.put(
            routing_key=self.queue_name,
            data={"key": "handler_with_requeue_then_ack"},
        )
        await asyncio.sleep(2)
        self.assertEqual(1, handler_with_requeue_called)
        await self.app.shutdown()

    async def test_process_message_reject_without_requeue(self):
        """
        Adicionamos um handler que causa uma falha mas que joga a mensagem fora.
        Temos que conferir que o handler foi chamado
        """

        @self.app.amqp.consume([self.queue_name])
        async def other_handler(messages):
            global handler_without_requeue_called
            handler_without_requeue_called += 1
            messages[0].reject(requeue=False)
            value = messages[0].field  # AttributeError

        await self.app.startup()
        queue = self.connection["/"]
        await queue.connection._connect()
        await queue.connection.channel.queue_declare(self.queue_name)

        await queue.put(
            routing_key=self.queue_name, data={"key": "handler_without_requeue"}
        )
        await asyncio.sleep(2)
        self.assertEqual(1, handler_without_requeue_called)

        await self.app.shutdown()
        await queue.connection.close()

        async def callback(*args, **kwargs):
            global consume_callback_shoud_not_be_called
            consume_callback_shoud_not_be_called = True

        queue = self.connection["/"]
        await queue.connection._connect()
        await queue.connection.channel.basic_consume(
            callback, queue_name=self.queue_name
        )
        await asyncio.sleep(5)
        self.assertFalse(consume_callback_shoud_not_be_called)


class AMQPConsumerTestWithAdditionalParameters(TestCase):
    maxDiff = None

    async def setUp(self):
        from aiohttp import ClientSession, BasicAuth

        client = ClientSession()

        await client.put(
            "http://127.0.0.1:15672/api/vhosts/logs",
            json={},
            auth=BasicAuth(login="guest", password="guest"),
        )
        resp = await client.put(
            "http://127.0.0.1:15672/api/permissions/logs/guest",
            json={"configure": ".*", "write": ".*", "read": ".*"},
            auth=BasicAuth(login="guest", password="guest"),
        )

    async def test_consume_one_message_app_with_multiple_connections(self):
        conn = AMQPConnection(
            hostname="127.0.0.1", username="guest", password="guest", prefetch=1
        )
        conn_2 = AMQPConnection(
            hostname="127.0.0.1:5673",
            username="guest",
            password="guest",
            prefetch=1,
        )
        await conn["/"].connection._connect()
        await conn["/"].connection.channel.queue_declare("queue")
        await conn["/"].put(data={"num": 42}, routing_key="queue")

        app = App(connections=[conn, conn_2])

        @app.amqp.consume(["queue"], connection=conn)
        async def handler(msgs):
            global message_processed_multiple_connections
            message_processed_multiple_connections = True

        await app.startup()
        await asyncio.sleep(1)
        await app.shutdown()
        self.assertTrue(message_processed_multiple_connections)

    async def test_consume_from_other_vhost(self):
        conn = AMQPConnection(
            hostname="127.0.0.1", username="guest", password="guest", prefetch=1
        )

        await conn["logs"].connection._connect()
        await conn["logs"].connection.channel.queue_declare("queue")
        await conn["logs"].put(data={"num": 42}, routing_key="queue")

        app = App(connections=[conn])

        @app.amqp.consume(["queue"], vhost="logs")
        async def handler(msgs):
            global message_processed_other_vhost
            message_processed_other_vhost = True

        await app.startup()
        await asyncio.sleep(1)
        await app.shutdown()
        self.assertTrue(message_processed_other_vhost)
