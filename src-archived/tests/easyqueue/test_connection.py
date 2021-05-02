import asyncio

import asynctest
from aioamqp.exceptions import AioamqpException
from asynctest import Mock, CoroutineMock, call, ANY, mock

from asyncworker.easyqueue.connection import AMQPConnection
from tests.easyqueue.base import AsyncBaseTestCase


class AMQPConnectionTests(AsyncBaseTestCase, asynctest.TestCase):
    async def setUp(self):
        super(AMQPConnectionTests, self).setUp()
        self.connection = AMQPConnection(**self.conn_params, on_error=Mock())

    async def test_connection_lock_ensures_amqp_connect_is_only_called_once(
        self
    ):
        transport = Mock()
        protocol = Mock(channel=CoroutineMock(is_open=True))

        conn = (transport, protocol)
        with asynctest.patch(
            "asyncworker.easyqueue.connection.aioamqp.connect",
            return_value=conn,
        ) as connect:
            await asyncio.gather(
                *(self.connection._connect() for _ in range(100))
            )
            self.assertEqual(connect.await_count, 1)

    async def test_connects_with_correct_args(self):

        await self.connection._connect()

        self.assertEqual(
            self._connect.call_args_list,
            [
                call(
                    host=self.conn_params["host"],
                    password=self.conn_params["password"],
                    virtualhost=self.conn_params["virtual_host"],
                    login=self.conn_params["username"],
                    on_error=self.connection._on_error,
                    loop=ANY,
                    heartbeat=self.conn_params["heartbeat"],
                )
            ],
        )
