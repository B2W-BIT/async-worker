from aioamqp.protocol import OPEN
from asynctest import TestCase

from asyncworker.easyqueue.queue import (
    JsonQueue,
    _ensure_conn_is_ready,
    ConnType,
)


class EnsureConnectedTest(TestCase):
    async def setUp(self):
        self.queue = JsonQueue(
            host="127.0.0.1", username="guest", password="guest"
        )
        self.write_conn = self.queue.conn_for(ConnType.WRITE)
        self.wrapped = _ensure_conn_is_ready(ConnType.WRITE)(self._func)

    async def _func(self, arg1):
        return 42

    async def tearDown(self):
        await self.write_conn.close()

    async def test_create_new_channel_if_channel_is_closed(self):
        await self.wrapped(self.queue)

        await self.write_conn.channel.close()

        channel, proto, transp = (
            self.write_conn.channel,
            self.write_conn._protocol,
            self.write_conn._transport,
        )

        self.assertEqual(42, await self.wrapped(self.queue))

        self.assertNotEqual(channel, self.write_conn.channel)
        self.assertEqual(proto, self.write_conn._protocol)
        self.assertEqual(transp, self.write_conn._transport)

    async def test_do_nothing_if_protocol_and_channel_are_open(self):
        await self.wrapped(self.queue)

        channel, proto, transp = (
            self.write_conn.channel,
            self.write_conn._protocol,
            self.write_conn._transport,
        )

        self.assertEqual(42, await self.wrapped(self.queue))

        self.assertEqual(channel, self.write_conn.channel)
        self.assertEqual(proto, self.write_conn._protocol)
        self.assertEqual(transp, self.write_conn._transport)

    async def test_recreate_connected_if_protocol_is_closed(self):
        await self.wrapped(self.queue)

        await self.write_conn.channel.close()
        await self.write_conn._protocol.close()
        channel, proto, transp = (
            self.write_conn.channel,
            self.write_conn._protocol,
            self.write_conn._transport,
        )

        self.assertEqual(42, await self.wrapped(self.queue))

        self.assertNotEqual(channel, self.write_conn.channel)
        self.assertNotEqual(proto, self.write_conn._protocol)
        self.assertNotEqual(transp, self.write_conn._transport)
        self.assertTrue(self.write_conn.channel.is_open)
        self.assertEqual(self.write_conn._protocol.state, OPEN)
