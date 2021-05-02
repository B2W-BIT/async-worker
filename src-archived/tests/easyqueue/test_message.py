from unittest.mock import Mock

import asynctest
from asynctest import CoroutineMock

from asyncworker.easyqueue.exceptions import UndecodableMessageException
from asyncworker.easyqueue.message import AMQPMessage


class AMQPMessageTests(asynctest.TestCase):
    def test_lazy_deserialization_raises_an_error_if_deserialization_fails(
        self
    ):
        data = b"Xablau"
        deserializer = Mock(side_effect=ValueError)

        msg = AMQPMessage(
            connection=Mock(),
            channel=Mock(),
            queue_name=Mock(),
            serialized_data=data,
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=deserializer,
            queue=Mock(),
        )

        with self.assertRaises(UndecodableMessageException):
            _ = msg.deserialized_data

        deserializer.assert_called_once_with(data)

    def test_successful_deserialization(self):
        data = b'["Xablau"]'
        deserializer = Mock(return_value=["Xablau"])

        msg = AMQPMessage(
            connection=Mock(),
            channel=Mock(),
            queue_name=Mock(),
            serialized_data=data,
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=deserializer,
            queue=Mock(),
        )

        self.assertEqual(msg.deserialized_data, ["Xablau"])

    def test_deserialization_is_only_called_once(self):
        data = b'["Xablau"]'
        deserializer = Mock(return_value=["Xablau"])

        msg = AMQPMessage(
            queue=Mock(),
            connection=Mock(),
            channel=Mock(),
            queue_name=Mock(),
            serialized_data=data,
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=deserializer,
        )

        _ = [msg.deserialized_data for _ in range(10)]

        deserializer.assert_called_once_with(data)

    def test_equal_messages(self):
        msg1 = AMQPMessage(
            connection=Mock(),
            channel=Mock(),
            queue_name=Mock(),
            serialized_data=Mock(),
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=Mock(),
            queue=Mock(),
        )
        msg2 = AMQPMessage(
            connection=msg1.connection,
            channel=msg1.channel,
            queue_name=msg1.queue_name,
            serialized_data=msg1.serialized_data,
            delivery_tag=msg1.delivery_tag,
            envelope=msg1._envelope,
            properties=msg1._properties,
            deserialization_method=msg1._deserialization_method,
            queue=msg1._queue,
        )
        self.assertEqual(msg1, msg2)

    def test_not_equal_messages(self):
        msg1 = AMQPMessage(
            connection=Mock(),
            channel=Mock(),
            queue_name=Mock(),
            serialized_data=Mock(),
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=Mock(),
            queue=Mock(),
        )

        msg2 = AMQPMessage(
            connection=msg1.connection,
            channel=Mock(),
            queue_name=msg1.queue_name,
            serialized_data=msg1.serialized_data,
            delivery_tag=msg1.delivery_tag,
            envelope=msg1._envelope,
            properties=msg1._properties,
            deserialization_method=msg1._deserialization_method,
            queue=Mock(),
        )
        self.assertNotEqual(msg1, msg2)

    async def test_it_acks_messages(self):
        msg = AMQPMessage(
            connection=Mock(),
            channel=Mock(basic_client_ack=CoroutineMock()),
            queue_name=Mock(),
            serialized_data=Mock(),
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=Mock(),
            queue=Mock(),
        )
        await msg.ack()

        msg.channel.basic_client_ack.assert_awaited_once_with(msg.delivery_tag)

    async def test_it_rejects_messages_without_requeue(self):
        msg = AMQPMessage(
            connection=Mock(),
            channel=Mock(basic_reject=CoroutineMock()),
            queue_name=Mock(),
            serialized_data=Mock(),
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=Mock(),
            queue=Mock(),
        )

        await msg.reject()

        msg.channel.basic_reject.assert_awaited_once_with(
            delivery_tag=msg.delivery_tag, requeue=False
        )

    async def test_it_rejects_messages_with_requeue(self):
        msg = AMQPMessage(
            connection=Mock(),
            channel=Mock(basic_reject=CoroutineMock()),
            queue_name=Mock(),
            serialized_data=Mock(),
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=Mock(),
            queue=Mock(),
        )

        await msg.reject(requeue=True)
        msg.channel.basic_reject.assert_awaited_once_with(
            delivery_tag=msg.delivery_tag, requeue=True
        )
