from typing import Any

from aioamqp.exceptions import ChannelClosed
from asynctest import TestCase

from asyncworker.easyqueue.message import AMQPMessage
from asyncworker.easyqueue.queue import (
    ConnType,
    JsonQueue,
    QueueConsumerDelegate,
)


class DumbConsumer(QueueConsumerDelegate):
    async def on_queue_message(self, msg: AMQPMessage[Any]):
        pass


class JsonQueueTest(TestCase):
    async def setUp(self):
        self.queue = JsonQueue(
            "127.0.0.1", "guest", "guest", delegate=DumbConsumer()
        )
        self.consume_conn = self.queue.conn_for(ConnType.CONSUME)
        self.write_conn = self.queue.conn_for(ConnType.WRITE)

    async def test_put_doesn_connect_consume_connection(self):
        """
        Certifica que uma Queue que faz apenas escrita não abre a conexão
        de consumers. Abre apenas a conexão de escrita.
        """

        self.assertFalse(self.consume_conn.is_connected)
        self.assertIsNone(self.consume_conn.channel)

        await self.queue.put(routing_key="some-queue", data={"OK": True})

        self.assertTrue(self.write_conn.is_connected, "Não abriu a write conn")
        self.assertTrue(self.write_conn.channel.is_open)

        self.assertFalse(
            self.consume_conn.is_connected,
            "Conectou a consume conn, não deveria",
        )
        self.assertIsNone(self.consume_conn.channel)

    async def test_consume_doesnt_open_write_connection(self):
        """
        Certifica que se uma queue faz apenas consume ela não 
        abre a conexão que é dedicada a escrita.
        """
        self.assertFalse(self.consume_conn.is_connected)
        self.assertIsNone(self.consume_conn.channel)

        with self.assertRaises(ChannelClosed):
            await self.queue.consume("some-queue", DumbConsumer())

        self.assertTrue(
            self.consume_conn.is_connected, "Não connectou a consume connection"
        )
        self.assertIsNotNone(self.consume_conn.channel)

        self.assertFalse(
            self.write_conn.is_connected,
            "Conectou a write connection, não deveria",
        )
        self.assertIsNone(self.write_conn.channel)

    async def test_get_conn_for_consume(self):
        self.assertEqual(
            self.queue.connection, self.queue.conn_for(ConnType.CONSUME)
        )

    async def test_get_conn_for_write(self):
        self.assertEqual(
            self.queue._write_connection, self.queue.conn_for(ConnType.WRITE)
        )
