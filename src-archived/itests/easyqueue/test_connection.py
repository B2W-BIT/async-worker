from aioamqp.protocol import OPEN
from asynctest import TestCase

from asyncworker.easyqueue.connection import AMQPConnection


class ConnectionTest(TestCase):
    async def setUp(self):
        self.conn = AMQPConnection("127.0.0.1", "guest", "guest")

    async def tearDown(self):
        await self.conn.close()

    async def test_can_call_close_multiple_times(self):
        await self.conn._connect()
        self.assertTrue(self.conn.is_connected)

        await self.conn.close()
        await self.conn.close()

        self.assertFalse(self.conn.is_connected)
        self.assertFalse(self.conn.channel.is_open)
        self.assertNotEqual(self.conn._protocol.state, OPEN)

    async def test_has_channel_ready(self):

        await self.conn._connect()
        self.assertTrue(self.conn.has_channel_ready())

        await self.conn.channel.close()

        self.assertTrue(self.conn.is_connected)
        self.assertFalse(self.conn.has_channel_ready())

    async def test_call_connect_channel_closed_protocol_raised_aioamqp_exception(
        self
    ):
        await self.conn._connect()

        await self.conn.channel.close()
        await self.conn.close()
        self.assertFalse(self.conn.channel.is_open)
        self.assertFalse(self.conn.is_connected)
        self.assertFalse(self.conn.has_channel_ready())

        channel, proto, transp = (
            self.conn.channel,
            self.conn._protocol,
            self.conn._transport,
        )

        await self.conn._connect()

        self.assertNotEqual(proto, self.conn._protocol)
        self.assertNotEqual(transp, self.conn._transport)
        self.assertNotEqual(channel, self.conn.channel)

        self.assertTrue(self.conn.channel.is_open)
        self.assertEqual(self.conn._protocol.state, OPEN)

    async def test_call_connect_with_channel_closed_has_protocol(self):
        await self.conn._connect()

        await self.conn.channel.close()
        self.assertFalse(self.conn.channel.is_open)

        channel, proto, transp = (
            self.conn.channel,
            self.conn._protocol,
            self.conn._transport,
        )

        await self.conn._connect()

        self.assertEqual(proto, self.conn._protocol)
        self.assertEqual(transp, self.conn._transport)
        self.assertNotEqual(channel, self.conn.channel)

        self.assertTrue(self.conn.channel.is_open)
