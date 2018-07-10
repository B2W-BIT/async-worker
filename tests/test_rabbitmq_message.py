import asynctest
from asynctest.mock import CoroutineMock
from asynctest import mock

from asyncworker.rabbitmq import RabbitMQMessage
from asyncworker.options import Events, Actions

class RabbitMQMessageTest(asynctest.TestCase):

    def setUp(self):
        self.queue_mock = CoroutineMock(ack=CoroutineMock(), reject=CoroutineMock())

    async def test_process_success_default_action(self):
        """
        Default é ACK, caso não digamos nada
        """
        message = RabbitMQMessage(body={}, delivery_tag=10)

        await message.process_success(self.queue_mock)
        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)
        self.queue_mock.reject.assert_not_awaited()

    async def test_process_success_action_ack(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.ACK)

        await message.process_success(self.queue_mock)
        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)
        self.queue_mock.reject.assert_not_awaited()

    async def test_process_success_action_reject(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.REJECT)

        await message.process_success(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=False)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_success_action_requeue(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.REQUEUE)

        await message.process_success(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_success_from_ack_to_requeue(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.ACK)
        message.reject(requeue=True)
        await message.process_success(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_success_from_ack_to_reject(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.ACK)
        message.reject(requeue=False)
        await message.process_success(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=False)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_success_from_reject_to_ack(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.REJECT)
        message.accept()
        await message.process_success(self.queue_mock)
        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)
        self.queue_mock.reject.assert_not_awaited()

    async def test_process_success_from_reject_to_requeue(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.REJECT)
        message.reject(requeue=True)
        await message.process_success(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_success_from_requeue_to_ack(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.REQUEUE)
        message.accept()
        await message.process_success(self.queue_mock)
        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)
        self.queue_mock.reject.assert_not_awaited()

    async def test_process_success_from_requeue_to_reject(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_success=Actions.REQUEUE)
        message.reject(requeue=False)
        await message.process_success(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=False)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_exception_default_action(self):
        message = RabbitMQMessage(body={}, delivery_tag=10)

        await message.process_exception(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_exception_action_requeue(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.REQUEUE)

        await message.process_exception(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_exception_action_ack(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.ACK)

        await message.process_exception(self.queue_mock)
        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)
        self.queue_mock.reject.assert_not_awaited()

    async def test_process_exception_action_reject(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.REJECT)

        await message.process_exception(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=False)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_exception_from_ack_to_requeue(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.ACK)
        message.reject(requeue=True)

        await message.process_exception(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_exception_from_ack_to_reject(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.ACK)
        message.reject(requeue=False)

        await message.process_exception(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=False)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_exception_from_reject_to_ack(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.REJECT)
        message.accept()

        await message.process_exception(self.queue_mock)
        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)
        self.queue_mock.reject.assert_not_awaited()

    async def test_process_exception_from_reject_to_requeue(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.REJECT)
        message.reject(requeue=True)

        await message.process_exception(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)
        self.queue_mock.ack.assert_not_awaited()

    async def test_process_exception_from_requeue_to_ack(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.REQUEUE)
        message.accept()

        await message.process_exception(self.queue_mock)
        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)
        self.queue_mock.reject.assert_not_awaited()

    async def test_process_exception_from_requeue_to_reject(self):
        message = RabbitMQMessage(body={}, delivery_tag=10, on_exception=Actions.REQUEUE)
        message.reject(requeue=False)

        await message.process_exception(self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=False)
        self.queue_mock.ack.assert_not_awaited()

