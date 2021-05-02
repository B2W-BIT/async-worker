import json

import asynctest
from asynctest.mock import CoroutineMock, Mock

from asyncworker.easyqueue.message import AMQPMessage
from asyncworker.options import Actions
from asyncworker.rabbitmq import RabbitMQMessage


class RabbitMQMessageTest(asynctest.TestCase):
    def setUp(self):
        self.amqp_message = Mock(ack=CoroutineMock(), reject=CoroutineMock())

    async def test_process_success_default_action(self):
        """
        ACK is the default action
        """
        message = RabbitMQMessage(
            delivery_tag=10, amqp_message=self.amqp_message
        )

        await message.process_success()
        self.amqp_message.ack.assert_awaited_with()
        self.amqp_message.reject.assert_not_awaited()

    async def test_process_success_action_ack(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.ACK,
            amqp_message=self.amqp_message,
        )

        await message.process_success()
        self.amqp_message.ack.assert_awaited_with()
        self.amqp_message.reject.assert_not_awaited()

    async def test_process_success_action_reject(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.REJECT,
            amqp_message=self.amqp_message,
        )

        await message.process_success()
        self.amqp_message.reject.assert_awaited_with(requeue=False)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_success_action_requeue(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.REQUEUE,
            amqp_message=self.amqp_message,
        )

        await message.process_success()
        self.amqp_message.reject.assert_awaited_with(requeue=True)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_success_from_ack_to_requeue(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.ACK,
            amqp_message=self.amqp_message,
        )
        message.reject(requeue=True)
        await message.process_success()
        self.amqp_message.reject.assert_awaited_with(requeue=True)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_success_from_ack_to_reject(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.ACK,
            amqp_message=self.amqp_message,
        )
        message.reject(requeue=False)
        await message.process_success()
        self.amqp_message.reject.assert_awaited_with(requeue=False)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_success_from_reject_to_ack(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.REJECT,
            amqp_message=self.amqp_message,
        )
        message.accept()
        await message.process_success()
        self.amqp_message.ack.assert_awaited_with()
        self.amqp_message.reject.assert_not_awaited()

    async def test_process_success_from_reject_to_requeue(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.REJECT,
            amqp_message=self.amqp_message,
        )
        message.reject(requeue=True)
        await message.process_success()
        self.amqp_message.reject.assert_awaited_with(requeue=True)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_success_from_requeue_to_ack(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.REQUEUE,
            amqp_message=self.amqp_message,
        )
        message.accept()
        await message.process_success()
        self.amqp_message.ack.assert_awaited_with()
        self.amqp_message.reject.assert_not_awaited()

    async def test_process_success_from_requeue_to_reject(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_success=Actions.REQUEUE,
            amqp_message=self.amqp_message,
        )
        message.reject(requeue=False)
        await message.process_success()
        self.amqp_message.reject.assert_awaited_with(requeue=False)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_exception_default_action(self):
        message = RabbitMQMessage(
            delivery_tag=10, amqp_message=self.amqp_message
        )

        await message.process_exception()
        self.amqp_message.reject.assert_awaited_with(requeue=True)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_exception_action_requeue(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.REQUEUE,
            amqp_message=self.amqp_message,
        )

        await message.process_exception()
        self.amqp_message.reject.assert_awaited_with(requeue=True)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_exception_action_ack(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.ACK,
            amqp_message=self.amqp_message,
        )

        await message.process_exception()
        self.amqp_message.ack.assert_awaited_with()
        self.amqp_message.reject.assert_not_awaited()

    async def test_process_exception_action_reject(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.REJECT,
            amqp_message=self.amqp_message,
        )

        await message.process_exception()
        self.amqp_message.reject.assert_awaited_with(requeue=False)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_exception_from_ack_to_requeue(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.ACK,
            amqp_message=self.amqp_message,
        )
        message.reject(requeue=True)

        await message.process_exception()
        self.amqp_message.reject.assert_awaited_with(requeue=True)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_exception_from_ack_to_reject(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.ACK,
            amqp_message=self.amqp_message,
        )
        message.reject(requeue=False)

        await message.process_exception()
        self.amqp_message.reject.assert_awaited_with(requeue=False)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_exception_from_reject_to_ack(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.REJECT,
            amqp_message=self.amqp_message,
        )
        message.accept()

        await message.process_exception()
        self.amqp_message.ack.assert_awaited_with()
        self.amqp_message.reject.assert_not_awaited()

    async def test_process_exception_from_reject_to_requeue(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.REJECT,
            amqp_message=self.amqp_message,
        )
        message.reject(requeue=True)

        await message.process_exception()
        self.amqp_message.reject.assert_awaited_with(requeue=True)
        self.amqp_message.ack.assert_not_awaited()

    async def test_process_exception_from_requeue_to_ack(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.REQUEUE,
            amqp_message=self.amqp_message,
        )
        message.accept()

        await message.process_exception()
        self.amqp_message.ack.assert_awaited_with()
        self.amqp_message.reject.assert_not_awaited()

    async def test_process_exception_from_requeue_to_reject(self):
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.REQUEUE,
            amqp_message=self.amqp_message,
        )
        message.reject(requeue=False)

        await message.process_exception()
        self.amqp_message.reject.assert_awaited_with(requeue=False)
        self.amqp_message.ack.assert_not_awaited()

    def test_serialized_data_property(self):
        amqp_message = AMQPMessage(
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
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.REQUEUE,
            amqp_message=amqp_message,
        )
        self.assertEqual(message.serialized_data, amqp_message.serialized_data)

    def test_body_property(self):
        amqp_message = AMQPMessage(
            connection=Mock(),
            channel=Mock(),
            queue_name=Mock(),
            serialized_data='["Xablau", "Xena"]',
            delivery_tag=Mock(),
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=json.loads,
            queue=Mock(),
        )
        message = RabbitMQMessage(
            delivery_tag=10,
            on_exception=Actions.REQUEUE,
            amqp_message=amqp_message,
        )
        self.assertEqual(message.body, ["Xablau", "Xena"])
