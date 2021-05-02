import json
import logging
from unittest.mock import patch, call, ANY, Mock

import aioamqp
import asynctest
from aioamqp.channel import Channel
from asynctest.mock import CoroutineMock, Mock, MagicMock

from asyncworker.easyqueue.message import AMQPMessage
from asyncworker.easyqueue.queue import (
    ConnType,
    _ensure_conn_is_ready,
    _ConsumptionHandler,
    JsonQueue,
    QueueConsumerDelegate,
)


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
        self.write_conn = self.queue.conn_for(ConnType.WRITE)
        self.consume_conn = self.queue.conn_for(ConnType.CONSUME)
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
                basic_consume=CoroutineMock(
                    return_value={"consumer_tag": self.consumer_tag}
                ),
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
        raise NotImplementedError


class AsynQueueTests(asynctest.TestCase):
    async def test_it_raises_an_error_if_its_initialized_with_both_delegate_and_delegate_class(
        self
    ):
        with self.assertRaises(ValueError):
            JsonQueue(
                host="diogommartins.com",
                username="diogo",
                password="XablauBolado",
                loop=Mock(),
                delegate=Mock(),
                delegate_class=Mock(),
            )

    async def test_its_possibile_to_initialize_without_a_delegate(self):
        queue = JsonQueue(
            host="diogommartins.com",
            username="diogo",
            password="XablauBolado",
            loop=Mock(),
        )
        self.assertIsInstance(queue, JsonQueue)

    async def test_it_initializes_a_delegate_if_delegate_class_is_provided(
        self
    ):
        delegate_class = Mock()
        JsonQueue(Mock(), Mock(), Mock(), delegate_class=delegate_class)
        delegate_class.assert_called_once_with()


class AsyncQueueConnectionTests(AsyncBaseTestCase, asynctest.TestCase):
    def get_consumer(self):
        return CoroutineMock()

    async def test_it_dosent_call_consumer_handler_methods(self):
        self.assertFalse(self.queue.delegate.on_queue_message.called)

    async def test_it_puts_messages_into_queue_as_json_if_message_is_a_json_serializeable(
        self
    ):
        message = {
            "artist": "Great White",
            "song": "Once Bitten Twice Shy",
            "album": "Twice Shy",
        }
        exchange = Mock()
        routing_key = Mock()
        properties = Mock()
        mandatory = Mock()
        immediate = Mock()
        await self.queue.put(
            data=message,
            exchange=exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )

        expected = call(
            payload=json.dumps(message).encode(),
            routing_key=routing_key,
            exchange_name=exchange,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )
        self.assertEqual(
            [expected], self.write_conn.channel.publish.call_args_list
        )

    async def test_it_puts_messages_into_queue_as_is_if_message_is_already_a_json(
        self
    ):
        message = {
            "artist": "Great White",
            "song": "Once Bitten Twice Shy",
            "album": "Twice Shy",
        }
        exchange = Mock()
        routing_key = Mock()
        properties = Mock()
        mandatory = Mock()
        immediate = Mock()
        await self.queue.put(
            serialized_data=json.dumps(message),
            exchange=exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )

        expected = call(
            payload=json.dumps(message).encode(),
            routing_key=routing_key,
            exchange_name=exchange,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )
        self.assertEqual(
            [expected], self.write_conn.channel.publish.call_args_list
        )

    async def test_it_raises_an_error_if_both_data_and_json_are_passed_to_put_message(
        self
    ):
        message = {
            "artist": "Great White",
            "song": "Once Bitten Twice Shy",
            "album": "Twice Shy",
        }
        exchange = Mock()
        routing_key = Mock()
        properties = Mock()
        mandatory = Mock()
        immediate = Mock()
        with self.assertRaises(ValueError):
            await self.queue.put(
                serialized_data=json.dumps(message),
                data=message,
                exchange=exchange,
                routing_key=routing_key,
                properties=properties,
                mandatory=mandatory,
                immediate=immediate,
            )

        expected = call(
            payload=json.dumps(message).encode(),
            routing_key=routing_key,
            exchange_name=exchange,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )
        self.write_conn.channel.publish.assert_not_called()

    async def test_it_encodes_payload_into_bytes_if_payload_is_str(self):
        payload = json.dumps({"dog": "Xablau"})
        exchange = Mock()
        routing_key = Mock()
        properties = Mock()
        mandatory = Mock()
        immediate = Mock()
        await self.queue.put(
            serialized_data=payload,
            exchange=exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )

        self.write_conn.channel.publish.assert_awaited_once_with(
            payload=payload.encode(),
            routing_key=routing_key,
            exchange_name=exchange,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )

    async def test_it_doesnt_encodes_payload_into_bytes_if_payload_is_already_bytes(
        self
    ):
        payload = json.dumps({"dog": "Xablau"}).encode()
        exchange = Mock()
        routing_key = Mock()
        properties = Mock()
        mandatory = Mock()
        immediate = Mock()
        await self.queue.put(
            serialized_data=payload,
            exchange=exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )

        self.write_conn.channel.publish.assert_awaited_once_with(
            payload=payload,
            routing_key=routing_key,
            exchange_name=exchange,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )

    async def test_connect_gets_awaited_if_put_is_called_before_connect(self):

        message = {
            "artist": "Great White",
            "song": "Once Bitten Twice Shy",
            "album": "Twice Shy",
        }
        with asynctest.patch.object(
            self.write_conn, "_connect"
        ) as connect, asynctest.patch.object(
            self.write_conn,
            "channel",
            Mock(is_open=False, publish=CoroutineMock()),
        ):
            await self.queue.put(data=message, routing_key="Xablau")
            connect.assert_awaited_once()

    async def test_it_raises_and_error_if_put_message_isnt_json_serializeable(
        self
    ):
        message = Mock()

        exchange = Mock()
        routing_key = Mock()

        with self.assertRaises(TypeError):
            await self.queue.put(
                message, exchange=exchange, routing_key=routing_key
            )
        self.write_conn.channel.publish.assert_not_called()


class AsyncQueueConsumerTests(AsyncBaseTestCase, asynctest.TestCase):
    consumer_tag = "666"

    def get_consumer(self):
        return CoroutineMock(
            on_before_start_consumption=CoroutineMock(),
            on_consumption_start=CoroutineMock(),
        )

    async def test_it_calls_on_before_start_consumption_before_queue_consume(
        self
    ):
        await self.queue.connection._connect()

        with asynctest.patch.object(
            self.queue.connection.channel,
            "basic_consume",
            side_effect=Exception(),
        ):

            queue_name = Mock()
            self.queue.delegate.on_before_start_consumption.assert_not_called()
            with self.assertRaises(Exception):
                await self.queue.consume(queue_name, Mock())

            self.queue.delegate.on_before_start_consumption.called_once_with(
                queue_name, queue=self.queue
            )

    async def test_connect_gets_awaited_if_consume_is_called_before_connect(
        self
    ):
        channel = Mock(
            is_open=False,
            basic_qos=CoroutineMock(),
            basic_consume=CoroutineMock(),
        )
        with asynctest.patch.object(
            self.queue.connection, "_connect"
        ) as connect, asynctest.patch.object(
            self.queue.connection, "channel", channel
        ):
            queue_name = Mock()
            await self.queue.consume(
                queue_name, delegate=Mock(spec=QueueConsumerDelegate)
            )
            connect.assert_awaited_once()

    async def test_calling_consume_starts_message_consumption(self):
        await self.queue.connection._connect()
        await self.queue.consume(
            queue_name=Mock(), delegate=Mock(spec=QueueConsumerDelegate)
        )

        self.assertEqual(
            self.queue.connection.channel.basic_consume.call_count, 1
        )

    async def test_calling_consume_binds_handler_method(self):
        await self.queue.connection._connect()
        channel = self.queue.connection.channel

        queue_name = Mock()
        consumer_name = Mock()
        expected_prefetch_count = 666

        self.queue.prefetch_count = expected_prefetch_count
        with patch(
            "asyncworker.easyqueue.queue._ConsumptionHandler",
            return_value=Mock(spec=_ConsumptionHandler),
        ) as Handler:
            delegate = Mock(spec=QueueConsumerDelegate)
            await self.queue.consume(
                queue_name=queue_name,
                consumer_name=consumer_name,
                delegate=delegate,
            )

            expected = call(
                callback=ANY, queue_name=queue_name, consumer_tag=consumer_name
            )
            self.assertEqual(
                [expected],
                self.queue.connection.channel.basic_consume.call_args_list,
            )
            _, kwargs = channel.basic_consume.call_args_list[0]
            callback = kwargs["callback"]

            channel = Mock()
            body = Mock()
            envelope = Mock()
            properties = Mock()
            await callback(
                channel=channel,
                body=body,
                envelope=envelope,
                properties=properties,
            )
            Handler.assert_called_once_with(
                delegate=delegate, queue=self.queue, queue_name=queue_name
            )
            Handler.return_value.handle_message.assert_awaited_once_with(
                channel=channel,
                body=body,
                envelope=envelope,
                properties=properties,
            )

    async def test_calling_consume_sets_a_prefetch_qos(self):
        await self.queue.connection._connect()

        expected_prefetch_count = 666
        self.queue.prefetch_count = expected_prefetch_count
        await self.queue.consume(
            queue_name=Mock(), delegate=Mock(spec=QueueConsumerDelegate)
        )

        expected = call(
            connection_global=ANY,
            prefetch_count=expected_prefetch_count,
            prefetch_size=0,
        )
        self.assertEqual(
            [expected], self.queue.connection.channel.basic_qos.call_args_list
        )

    async def test_calling_consume_starts_a_connection(self):
        consumer = Mock(spec=QueueConsumerDelegate)
        self.assertFalse(self._connect.called)
        await self.queue.consume(
            queue_name=self.test_queue_name, delegate=consumer
        )
        self.assertTrue(self._connect.called)

    async def test_calling_consume_notifies_delegate(self):
        expected_prefetch_count = 666
        self.queue.prefetch_count = expected_prefetch_count
        delegate = Mock(spec=QueueConsumerDelegate)
        await self.queue.consume(
            queue_name=self.test_queue_name, delegate=delegate
        )

        delegate.on_before_start_consumption.assert_awaited_once_with(
            queue_name=self.test_queue_name, queue=self.queue
        )
        delegate.on_consumption_start.assert_awaited_once_with(
            consumer_tag=self.consumer_tag, queue=self.queue
        )


class AsyncQueueConsumerHandlerMethodsTests(
    AsyncBaseTestCase, asynctest.TestCase
):
    consumer_tag = "666"

    def get_consumer(self):
        return Mock(spec=QueueConsumerDelegate)

    async def setUp(self):
        super().setUp()
        self.properties = Mock(name="Properties")
        self.delegate = Mock(spec=QueueConsumerDelegate)
        consumer_tag = await self.queue.consume(
            queue_name=self.test_queue_name,
            delegate=self.delegate,
            consumer_name=self.__class__.__name__,
        )
        self.envelope = Mock(name="Envelope", consumer_tag=consumer_tag)
        self.handler = _ConsumptionHandler(
            delegate=self.delegate,
            queue=self.queue,
            queue_name=self.test_queue_name,
        )

    async def test_it_calls_on_queue_message_with_the_message_body_wrapped_as_a_AMQPMessage_instance(
        self
    ):
        content = {
            "artist": "Caetano Veloso",
            "song": "Não enche",
            "album": "Livro",
        }
        body = json.dumps(content).encode("utf-8")
        with patch.object(
            self.handler, "_handle_callback", CoroutineMock()
        ) as _handle_callback:
            await self.handler.handle_message(
                channel=self.queue.connection.channel,
                body=body,
                envelope=self.envelope,
                properties=self.properties,
            )

            _handle_callback.assert_called_once_with(
                self.handler.delegate.on_queue_message,
                msg=AMQPMessage(
                    connection=self.queue.connection,
                    channel=self.queue.connection.channel,
                    queue=self.queue,
                    envelope=self.envelope,
                    properties=self.properties,
                    delivery_tag=self.envelope.delivery_tag,
                    deserialization_method=self.queue.deserialize,
                    queue_name=self.test_queue_name,
                    serialized_data=body,
                ),
            )

    async def test_it_calls_on_message_handle_error_if_message_handler_raises_an_error(
        self
    ):
        content = {
            "artist": "Caetano Veloso",
            "song": "Não enche",
            "album": "Livro",
        }

        error = self.handler.delegate.on_queue_message.side_effect = KeyError()
        kwargs = dict(
            callback=self.handler.delegate.on_queue_message,
            channel=self.queue.connection.channel,
            body=json.dumps(content),
            envelope=self.envelope,
            properties=self.properties,
        )
        await self.handler._handle_callback(**kwargs)

        del kwargs["callback"]

        self.handler.delegate.on_message_handle_error.assert_called_once_with(
            handler_error=error, **kwargs
        )


class EnsureConnectedDecoratorTests(asynctest.TestCase):
    async def setUp(self):
        self.seconds = 666
        self.queue = JsonQueue(
            "127.0.0.1",
            "guest",
            "guest",
            seconds_between_conn_retry=self.seconds,
            logger=Mock(spec=logging.Logger),
            connection_fail_callback=CoroutineMock(),
        )

    async def test_it_waits_before_trying_to_reconnect_if_connect_fails(self):

        coro = CoroutineMock()
        with asynctest.patch(
            "asyncworker.easyqueue.queue.asyncio.sleep"
        ) as sleep, asynctest.patch.object(
            self.queue.connection,
            "_connect",
            CoroutineMock(side_effect=[ConnectionError, True]),
        ):
            wrapped = _ensure_conn_is_ready(ConnType.CONSUME)(coro)
            await wrapped(self.queue, 1, dog="Xablau")
            sleep.assert_awaited_once_with(self.seconds)

            # todo: CoroutineMock.side_effect is raised only on call, not on await
            self.queue.connection._connect.assert_has_awaits([call()])
            self.queue.connection._connect.assert_has_calls([call(), call()])
            coro.assert_awaited_once_with(self.queue, 1, dog="Xablau")

    async def test_it_logs_connection_retries_if_a_logger_istance_is_available(
        self
    ):
        coro = CoroutineMock()
        with asynctest.patch(
            "asyncworker.easyqueue.queue.asyncio.sleep"
        ), asynctest.patch.object(
            self.queue.connection,
            "_connect",
            CoroutineMock(side_effect=[ConnectionError, True]),
        ):

            wrapped = _ensure_conn_is_ready(ConnType.CONSUME)(coro)
            await wrapped(self.queue, 1, dog="Xablau")

            self.queue.logger.error.assert_called_once()

    async def test_it_calls_connection_fail_callback_if_connect_fails(self):
        error = ConnectionError()
        coro = CoroutineMock()
        with asynctest.patch(
            "asyncworker.easyqueue.queue.asyncio.sleep"
        ), asynctest.patch.object(
            self.queue.connection,
            "_connect",
            CoroutineMock(side_effect=[error, True]),
        ):
            wrapped = _ensure_conn_is_ready(ConnType.CONSUME)(coro)
            await wrapped(self.queue, 1, dog="Xablau")

            self.queue.connection_fail_callback.assert_awaited_once_with(
                error, 1
            )
