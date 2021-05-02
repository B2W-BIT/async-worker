import asyncio
import unittest

import asynctest
from aioamqp.exceptions import AioamqpException
from asynctest import CoroutineMock, Mock, mock

from asyncworker import App, conf
from asyncworker.bucket import Bucket
from asyncworker.connections import AMQPConnection
from asyncworker.consumer import Consumer
from asyncworker.easyqueue.message import AMQPMessage
from asyncworker.easyqueue.queue import JsonQueue
from asyncworker.options import Actions, Events, RouteTypes
from asyncworker.rabbitmq import AMQPRouteOptions


async def _handler(message):
    return (42, message[0].body)


class ConsumerTest(asynctest.TestCase):
    use_default_loop = True

    def setUp(self):
        self.queue_mock = Mock(
            connection=Mock(has_channel_ready=Mock(return_value=True)),
            spec=JsonQueue,
        )
        self.logger_mock = CoroutineMock(
            info=CoroutineMock(), debug=CoroutineMock(), error=CoroutineMock()
        )
        self.connection_parameters = ("127.0.0.1", "guest", "guest", 1024)
        self.one_route_fixture = {
            "routes": ["/asgard/counts/ok"],
            "handler": _handler,
            "vhost": "/",
            "options": {
                "bulk_size": 1,
                "bulk_flush_interval": 1,
                Events.ON_SUCCESS: Actions.ACK,
                Events.ON_EXCEPTION: Actions.REQUEUE,
            },
        }
        self.connection = AMQPConnection(
            hostname="127.0.0.1",
            username="guest",
            password="guest",
            prefetch=1024,
        )
        self.app = App(connections=[self.connection])
        self.mock_message = self._make_msg()
        mock.patch.object(
            conf, "settings", mock.Mock(FLUSH_TIMEOUT=0.1)
        ).start()

    def _make_msg(self, **kwargs) -> AMQPMessage:
        default_kwargs = dict(
            delivery_tag=10,
            connection=self.queue_mock.connection,
            channel=Mock(),
            queue=self.queue_mock,
            envelope=Mock(),
            properties=Mock(),
            deserialization_method=Mock(),
            queue_name="queue_name",
            serialized_data=Mock(),
        )
        return Mock(spec=AMQPMessage, **{**default_kwargs, **kwargs})

    def tearDown(self):
        mock.patch.stopall()

    def test_consumer_adjusts_bulk_size(self):
        """
        Se escolhermos um prefetch menor do que o bulk_size, significa que nosso "bucket"
        nunca vai encher e isso significa que nosso consumer ficará congelado, em um deadlock:
            Ele estará esperando o bucket encher
            E ao mesmo tempo estará o esperando o bucket esvaziar para que possa receber mais mensagens do RabbitMQ


        Vamos setar o bulk_size com sendo min(bulk_size, prefetch_count)
        """
        self.one_route_fixture["options"]["bulk_size"] = 2048
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.assertEqual(1024, consumer.bucket.size)

        self.one_route_fixture["options"]["bulk_size"] = 4096
        consumer = Consumer(
            self.one_route_fixture,
            host="127.0.0.1",
            username="guest",
            password="guest",
            prefetch_count=8192,
        )
        self.assertEqual(4096, consumer.bucket.size)

    def test_consumer_instantiate_using_bucket_class(self):
        class MyBucket(Bucket):
            pass

        consumer = Consumer(
            self.one_route_fixture,
            *self.connection_parameters,
            bucket_class=MyBucket,
        )
        self.assertTrue(isinstance(consumer.bucket, MyBucket))

    def test_consumer_instantiate_correct_size_bucket(self):
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.assertEqual(
            self.one_route_fixture["options"]["bulk_size"], consumer.bucket.size
        )

    def test_consumer_instantiate_async_queue_default_vhost(self):
        del self.one_route_fixture["vhost"]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        connection_parameters = consumer.queue.connection.connection_parameters

        self.assertTrue(isinstance(consumer.queue, JsonQueue))
        self.assertEqual("/", connection_parameters["virtualhost"])
        self.assertEqual("127.0.0.1", connection_parameters["host"])
        self.assertEqual("guest", connection_parameters["login"])
        self.assertEqual("guest", connection_parameters["password"])

    def test_consumer_instantiate_async_queue_other_vhost(self):
        self.one_route_fixture["vhost"] = "fluentd"
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        connection_parameters = consumer.queue.connection.connection_parameters

        self.assertTrue(isinstance(consumer.queue, JsonQueue))
        self.assertEqual("fluentd", connection_parameters["virtualhost"])

    def test_consumer_instantiate_async_queue_other_vhost_does_not_strip_slash(
        self
    ):
        self.one_route_fixture["vhost"] = "/fluentd"
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        connection_parameters = consumer.queue.connection.connection_parameters

        self.assertTrue(isinstance(consumer.queue, JsonQueue))
        self.assertEqual("/fluentd", connection_parameters["virtualhost"])

    def test_consumer_instantiate_async_queue_prefetch_count(self):
        self.one_route_fixture["vhost"] = "/fluentd"
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        connection_parameters = consumer.queue.connection.connection_parameters

        self.assertTrue(isinstance(consumer.queue, JsonQueue))
        self.assertEqual("/fluentd", connection_parameters["virtualhost"])
        self.assertEqual(1024, consumer.queue.prefetch_count)

    def test_consumer_returns_correct_queue_name(self):
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.assertEqual(["/asgard/counts/ok"], consumer.queue_name)

    async def test_on_queue_message_calls_inner_handler(self):
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        result = await consumer.on_queue_message(msg=self.mock_message)

        self.assertEqual((42, self.mock_message.deserialized_data), result)

    async def test_on_exception_requeue_message(self):
        """
        Confirma que em caso de exceção, será feito `message.reject(requeue=True)`
        """

        @self.app.amqp.consume(
            ["queue"], options=AMQPRouteOptions(on_exception=Actions.REQUEUE)
        )
        async def _handler(messages):
            raise Exception("BOOM!")

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        with self.assertRaises(Exception):
            await consumer.on_queue_message(msg=self.mock_message)
        self.mock_message.reject.assert_awaited_once_with(requeue=True)

    async def test_on_exception_reject_message(self):
        @self.app.amqp.consume(
            ["queue"], options=AMQPRouteOptions(on_exception=Actions.REJECT)
        )
        async def _handler(messages):
            raise Exception("BOOM!")

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        with self.assertRaises(Exception):
            await consumer.on_queue_message(msg=self.mock_message)
        self.mock_message.reject.assert_awaited_once_with(requeue=False)

    async def test_on_exception_ack_message(self):
        @self.app.amqp.consume(
            ["queue"], options=AMQPRouteOptions(on_exception=Actions.ACK)
        )
        async def _handler(messages):
            raise Exception("BOOM!")

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)
        with self.assertRaises(Exception):
            await consumer.on_queue_message(msg=self.mock_message)

        self.mock_message.ack.assert_awaited_once()

    async def test_on_success_ack(self):
        @self.app.amqp.consume(
            ["queue"], options=AMQPRouteOptions(on_success=Actions.ACK)
        )
        async def _handler(messages):
            return 42

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        await consumer.on_queue_message(msg=self.mock_message)
        self.mock_message.ack.assert_awaited_once()

    async def test_on_success_reject(self):
        @self.app.amqp.consume(
            ["queue"], options=AMQPRouteOptions(on_success=Actions.REJECT)
        )
        async def _handler(messages):
            return 42

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        await consumer.on_queue_message(msg=self.mock_message)
        self.mock_message.reject.assert_awaited_once_with(requeue=False)

    async def test_on_success_requeue(self):
        @self.app.amqp.consume(
            ["queue"], options=AMQPRouteOptions(on_success=Actions.REQUEUE)
        )
        async def _handler(messages):
            return 42

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        await consumer.on_queue_message(msg=self.mock_message)
        self.mock_message.reject.assert_awaited_once_with(requeue=True)

    async def test_on_queue_message_auto_ack_on_success(self):
        """
        Se o handler registrado no @app.amqp.consume() rodar com sucesso,
        devemos fazer o ack da mensagem
        """
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)

        result = await consumer.on_queue_message(msg=self.mock_message)

        self.assertEqual((42, self.mock_message.deserialized_data), result)
        self.mock_message.ack.assert_awaited_once_with()
        self.mock_message.reject.assert_not_awaited()

    async def test_on_exception_default_action_bulk_messages(self):
        """
        Se o handler der raise em qualquer exception, devemos
        dar reject() na mensagem
        """

        async def exception_handler(message):
            return message.do_not_exist

        self.one_route_fixture["handler"] = exception_handler
        self.one_route_fixture["options"]["bulk_size"] = 2

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)

        msgs = [self._make_msg(delivery_tag=1), self._make_msg(delivery_tag=2)]
        with self.assertRaises(AttributeError):
            await consumer.on_queue_message(msg=msgs[0])
            await consumer.on_queue_message(msg=msgs[1])

        msgs[0].reject.assert_awaited_once_with(requeue=True)
        msgs[1].reject.assert_awaited_once_with(requeue=True)

        msgs[0].ack.assert_not_awaited()
        msgs[1].ack.assert_not_awaited()

    async def test_on_queue_message_precondition_failed_on_ack(self):
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.mock_message.ack.side_effect = AioamqpException

        with self.assertRaises(AioamqpException):
            await consumer.on_queue_message(msg=self.mock_message)

    async def test_on_queue_message_bulk_size_one(self):
        class MyBucket(Bucket):
            def pop_all(self):
                return self._items

        handler_mock = CoroutineMock(__name__="handler")
        self.one_route_fixture["handler"] = handler_mock
        self.one_route_fixture["options"]["bulk_size"] = 1

        consumer = Consumer(
            self.one_route_fixture,
            *self.connection_parameters,
            bucket_class=MyBucket,
        )
        msg = self._make_msg(delivery_tag=20)
        await consumer.on_queue_message(msg=msg)
        handler_mock.assert_awaited_once_with(consumer.bucket._items)

        msg.ack.assert_awaited_once()
        msg.reject.assert_not_awaited()

    async def test_on_queue_message_bulk_size_bigger_than_one(self):
        """
        Confere que o handler real só é chamado quando o bucket atinge o limite máximo de
        tamanho. E que o handler é chamado com a lista de mensagens.
        * Bucket deve estart vazio após o "flush"
        """

        class MyBucket(Bucket):
            def pop_all(self):
                return self._items

        handler_mock = CoroutineMock(__name__="handler")
        self.one_route_fixture["handler"] = handler_mock
        self.one_route_fixture["options"]["bulk_size"] = 2

        consumer = Consumer(
            self.one_route_fixture,
            *self.connection_parameters,
            bucket_class=MyBucket,
        )
        msgs = [
            self._make_msg(delivery_tag=10),
            self._make_msg(delivery_tag=20),
        ]
        await consumer.on_queue_message(msg=msgs[0])
        handler_mock.assert_not_awaited()

        await consumer.on_queue_message(msg=msgs[1])
        handler_mock.assert_awaited_once_with(consumer.bucket._items)

        msgs[0].ack.assert_awaited_once()
        msgs[1].ack.assert_awaited_once()

        msgs[0].reject.assert_not_awaited()
        msgs[1].reject.assert_not_awaited()

    async def test_on_queue_message_bulk_mixed_ack_and_reject(self):
        async def handler(messages):
            messages[1].reject()
            messages[2].reject()

        self.one_route_fixture["handler"] = handler
        self.one_route_fixture["options"]["bulk_size"] = 5

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)

        msgs = [self._make_msg(delivery_tag=i) for i in range(5)]
        for msg in msgs:
            await consumer.on_queue_message(msg)

        await consumer.on_queue_message(self._make_msg(delivery_tag=10))
        await consumer.on_queue_message(self._make_msg(delivery_tag=11))
        await consumer.on_queue_message(self._make_msg(delivery_tag=12))
        await consumer.on_queue_message(self._make_msg(delivery_tag=13))
        await consumer.on_queue_message(self._make_msg(delivery_tag=14))

        msgs[0].ack.assert_awaited_once()
        msgs[3].ack.assert_awaited_once()
        msgs[4].ack.assert_awaited_once()

        msgs[1].reject.assert_awaited_once_with(requeue=True)
        msgs[2].reject.assert_awaited_once_with(requeue=True)

    async def test_on_queue_message_bulk_mixed_ack_and_reject_on_success_reject(
        self
    ):
        self.maxDiff = None

        async def handler(messages):
            messages[1].reject(requeue=True)
            messages[2].reject(requeue=True)

        self.one_route_fixture["handler"] = handler
        self.one_route_fixture["options"]["bulk_size"] = 5
        self.one_route_fixture["options"][Events.ON_SUCCESS] = Actions.REJECT

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)

        msgs = [self._make_msg(delivery_tag=i) for i in range(5)]
        for msg in msgs:
            await consumer.on_queue_message(msg)

        msgs[0].reject.assert_awaited_once_with(requeue=False)
        msgs[1].reject.assert_awaited_once_with(requeue=True)
        msgs[2].reject.assert_awaited_once_with(requeue=True)
        msgs[3].reject.assert_awaited_once_with(requeue=False)
        msgs[4].reject.assert_awaited_once_with(requeue=False)

    async def test_bulk_flushes_on_timeout_even_with_bucket_not_full(self):
        class MyBucket(Bucket):
            def pop_all(self):
                global items
                items = self._items
                self._items = []
                return items

        handler_mock = CoroutineMock(__name__="handler")
        self.one_route_fixture["handler"] = handler_mock
        self.one_route_fixture["options"]["bulk_size"] = 3

        consumer = Consumer(
            self.one_route_fixture,
            *self.connection_parameters,
            bucket_class=MyBucket,
        )

        msgs = [
            self._make_msg(delivery_tag=10),
            self._make_msg(delivery_tag=11),
        ]
        await consumer.on_queue_message(msgs[0])
        handler_mock.assert_not_awaited()

        await consumer.on_queue_message(msgs[1])
        handler_mock.assert_not_awaited()

        self.loop.create_task(consumer._flush_clocked())
        # Realizando sleep para devolver o loop para o clock
        await asyncio.sleep(0.1)

        handler_mock.assert_awaited_once_with(items)

        msgs[0].ack.assert_awaited_once()
        msgs[1].ack.assert_awaited_once()

        msgs[0].reject.assert_not_awaited()
        msgs[1].reject.assert_not_awaited()

    async def test_do_not_flush_if_bucket_is_already_empty_when_timeout_expires(
        self
    ):
        class MyBucket(Bucket):
            def pop_all(self):
                global items
                items = self._items
                self._items = []
                return items

        handler_mock = CoroutineMock()
        self.one_route_fixture["handler"] = handler_mock
        self.one_route_fixture["options"]["bulk_size"] = 3

        consumer = Consumer(
            self.one_route_fixture,
            *self.connection_parameters,
            bucket_class=MyBucket,
        )

        self.loop.create_task(consumer._flush_clocked())
        # Realizando sleep para devolver o loop para o clock
        await asyncio.sleep(0.1)
        self.assertEqual(0, handler_mock.await_count)

    async def test_clock_flush_dont_stop_on_exception_in_flush_clocked(self):
        class MyBucket(Bucket):
            def pop_all(self):
                global items
                items = self._items
                self._items = []
                return items

        async def handler(*args):
            raise Exception()

        self.one_route_fixture["handler"] = handler
        self.one_route_fixture["options"]["bulk_size"] = 3
        self.one_route_fixture["options"]["bulk_flush_interval"] = 0.1

        consumer = Consumer(
            self.one_route_fixture,
            *self.connection_parameters,
            bucket_class=MyBucket,
        )
        await consumer.on_queue_message(self._make_msg())
        self.loop.create_task(consumer._flush_clocked())
        self.assertEqual(0, consumer.clock.current_iteration)

        # Realizando sleep para devolver o loop para o clock
        await asyncio.sleep(0.1)
        self.assertEqual(1, consumer.clock.current_iteration)

        # Realizando sleep para devolver o loop para o clock
        await asyncio.sleep(0.3)
        self.assertGreaterEqual(consumer.clock.current_iteration, 2)
        await consumer.clock.stop()

    async def test_on_message_handle_error_logs_exception(self):
        """
        Logamos a exception lançada pelo handler.
        Aqui o try/except serve apenas para termos uma exception real, com traceback.
        """
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with mock.patch.object(conf, "logger", self.logger_mock):
            try:
                1 / 0
            except Exception as e:
                await consumer.on_message_handle_error(e)
                self.logger_mock.error.assert_awaited_with(
                    {
                        "exc_message": "division by zero",
                        "exc_traceback": mock.ANY,
                    }
                )

    async def test_on_connection_error_logs_exception(self):
        """
        Logamos qualquer erro de conexão com o Rabbit, inclusive acesso negado
        """
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with mock.patch.object(conf, "logger", self.logger_mock):
            try:
                1 / 0
            except Exception as e:
                await consumer.on_connection_error(e)
                self.logger_mock.error.assert_awaited_with(
                    {
                        "exc_message": "division by zero",
                        "exc_traceback": mock.ANY,
                    }
                )

    async def test_on_queue_error_logs_exception_and_acks_message(self):
        """
        Logamos qualquer erro de parsing/validação de mensagem
        """
        delivery_tag = 42
        body = "not a JSON"
        queue_mock = CoroutineMock(ack=CoroutineMock())

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with mock.patch.object(conf, "logger", self.logger_mock):
            await consumer.on_queue_error(
                body, delivery_tag, "Error: not a JSON", queue_mock
            )
            self.logger_mock.error.assert_awaited_with(
                {
                    "exception": "Error: not a JSON",
                    "original_msg": body,
                    "parse-error": True,
                }
            )
            queue_mock.ack.assert_awaited_once_with(delivery_tag=delivery_tag)

    def test_return_correct_queue_name(self):
        """
        consumer.quene_name deve retornar o nome da fila que está sendo consumida.
        """
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.assertEqual(self.one_route_fixture["routes"], consumer.queue_name)

    async def test_consume_all_queues(self):
        """
        """
        self.one_route_fixture["routes"] = [
            "asgard/counts",
            "asgard/counts/errors",
        ]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(consume=CoroutineMock())
        await consumer.consume_all_queues(queue_mock)

        queue_mock.consume.assert_has_awaits(
            [
                mock.call(queue_name="asgard/counts", delegate=consumer),
                mock.call(queue_name="asgard/counts/errors", delegate=consumer),
            ],
            any_order=True,
        )

    async def test_restart_all_consumers_if_channel_is_closed(self):
        """
        Se detectamos que o channel está fechado, devemos reiniciar todos os
        consumers. Isso vale pois atualmente todos eles compartilham o mesmo channel.
        """
        self.one_route_fixture["routes"] = [
            "asgard/counts",
            "asgard/counts/errors",
        ]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(consume=CoroutineMock())

        with asynctest.patch.object(
            consumer, "queue", queue_mock
        ), unittest.mock.patch.object(
            consumer, "keep_runnig", side_effect=[True, True, True, False]
        ), asynctest.patch.object(
            asyncio, "sleep"
        ) as sleep_mock, asynctest.patch.object(
            consumer, "clock_task", side_effect=[True, True]
        ), asynctest.patch.object(
            consumer.queue.connection,
            "has_channel_ready",
            Mock(side_effect=[False, True, False]),
        ):
            await consumer.start()

            queue_mock.consume.assert_has_awaits(
                [
                    mock.call(queue_name="asgard/counts", delegate=consumer),
                    mock.call(
                        queue_name="asgard/counts/errors", delegate=consumer
                    ),
                    mock.call(queue_name="asgard/counts", delegate=consumer),
                    mock.call(
                        queue_name="asgard/counts/errors", delegate=consumer
                    ),
                ],
                any_order=True,
            )

    async def test_start_always_calls_sleep(self):
        """
        Regression:
            O sleep deve ser chamado *sempre*, e não apenas quando há tentativa de conexão.
            Aqui, tentamos reconectar apenas uma vez, mas mesmo assim o sleep é chamado 3x, pois o loop principal
            roda 3x.
        """
        self.one_route_fixture["route"] = [
            "asgard/counts",
            "asgard/counts/errors",
        ]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with unittest.mock.patch.object(
            consumer, "keep_runnig", side_effect=[True, True, True, False]
        ), asynctest.patch.object(
            asyncio, "sleep"
        ) as sleep_mock, asynctest.patch.object(
            consumer, "clock_task", side_effect=[True, True]
        ):
            queue_mock = CoroutineMock(
                consume=CoroutineMock(), connect=CoroutineMock()
            )
            consumer.queue = queue_mock

            await consumer.start()
            self.assertEqual(3, sleep_mock.await_count)

    async def test_start_dont_created_clock_when_connection_failed(self):
        self.one_route_fixture["routes"] = [
            "asgard/counts",
            "asgard/counts/errors",
        ]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with unittest.mock.patch.object(
            consumer, "keep_runnig", side_effect=[True, True, True, False]
        ):
            queue_mock = CoroutineMock(
                consume=CoroutineMock(),
                connect=CoroutineMock(side_effect=[AioamqpException, True]),
            )
            consumer.queue = queue_mock

            await consumer.start()
        # Realizando sleep para devolver o loop para o clock
        await asyncio.sleep(0.1)
        self.assertIsNone(consumer.clock_task)
        await consumer.clock.stop()
        await asyncio.sleep(0.1)

    async def test_start_create_clock_flusher(self):
        self.one_route_fixture["routes"] = [
            "asgard/counts",
            "asgard/counts/errors",
        ]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with unittest.mock.patch.object(
            consumer, "keep_runnig", side_effect=[True, True, True, False]
        ):
            queue_mock = CoroutineMock(
                consume=CoroutineMock(),
                connection=Mock(
                    connect=CoroutineMock(side_effect=[AioamqpException, True]),
                    has_channel_ready=Mock(side_effect=[True, False, False]),
                ),
            )
            consumer.queue = queue_mock

            await consumer.start()
        # Realizando sleep para devolver o loop para o clock
        await asyncio.sleep(0.1)
        self.assertIsNotNone(consumer.clock_task)
        await consumer.clock.stop()
        await asyncio.sleep(0.1)

    async def test_start_dont_created_another_clock_when_restart(self):
        self.one_route_fixture["routes"] = [
            "asgard/counts",
            "asgard/counts/errors",
        ]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(
            consume=CoroutineMock(),
            connect=CoroutineMock(side_effect=[True, True]),
        )

        with unittest.mock.patch.object(
            consumer, "keep_runnig", side_effect=[True, False, True, False]
        ):
            consumer.queue = queue_mock

            await consumer.start()
            my_task = consumer.clock_task

            await consumer.start()

        # Realizando sleep para devolver o loop para o clock
        await asyncio.sleep(0.1)
        self.assertTrue(my_task is consumer.clock_task)
        await consumer.clock.stop()
        await asyncio.sleep(0.1)
