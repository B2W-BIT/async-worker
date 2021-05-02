from unittest.mock import patch

import aioamqp
from asynctest import CoroutineMock

from asyncworker.easyqueue.queue import JsonQueue, QueueConsumerDelegate


class AsyncBaseTestCase:
    test_queue_name = "test_queue"
    consumer_tag = "consumer_666"

    def setUp(self):
        self.conn_params = dict(
            host="money.que.é.good",
            username="nós",
            password="não",
            virtual_host="have",
            heartbeat=5,
        )
        self.queue = JsonQueue(**self.conn_params, delegate=self.get_consumer())
        self.mock_connection()

    def tearDown(self):
        self._connect_patch.stop()

    def mock_connection(self):
        class SubscriptableCoroutineMock(CoroutineMock):
            def __getitem__(_, item):
                if item == "consumer_tag":
                    return self.consumer_tag
                raise NotImplementedError

        self._transport = CoroutineMock(name="transport")
        self._protocol = CoroutineMock(name="protocol", close=CoroutineMock())
        self._protocol.channel = SubscriptableCoroutineMock(
            return_value=CoroutineMock(
                publish=CoroutineMock(),
                basic_qos=CoroutineMock(),
                basic_consume=CoroutineMock(),
            )
        )
        mocked_connection = CoroutineMock(
            return_value=[self._transport, self._protocol]
        )
        self._connect_patch = patch.object(
            aioamqp, "connect", mocked_connection
        )
        self._connect = self._connect_patch.start()

    def get_consumer(self) -> QueueConsumerDelegate:
        return CoroutineMock()
