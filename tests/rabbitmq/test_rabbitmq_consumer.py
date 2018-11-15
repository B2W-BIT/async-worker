import asyncio
import unittest
from unittest import mock
from asynctest import CoroutineMock
import asynctest
import importlib

from easyqueue import AsyncQueue
from aioamqp.exceptions import AioamqpException

from asyncworker.bucket import Bucket
from asyncworker.consumer import Consumer
import asyncworker.consumer
from asyncworker import conf, App
from asyncworker.rabbitmq.message import RabbitMQMessage
from asyncworker.options import Events, Actions



async def _handler(message):
    return (42, message[0].body)

class ConsumerTest(asynctest.TestCase):

    def setUp(self):
        self.queue_mock = CoroutineMock(ack=CoroutineMock(), reject=CoroutineMock())
        self.connection_parameters = ("127.0.0.1", "guest", "guest", 1024)
        self.one_route_fixture = {
            "routes": ["/asgard/counts/ok"],
            "handler": _handler,
            "options": {
                "vhost": "/",
                "bulk_size": 1,
                "bulk_flush_interval": 60,
                Events.ON_SUCCESS: Actions.ACK,
                Events.ON_EXCEPTION: Actions.REQUEUE,
            }
        }
        self.app = App(**{"host": "127.0.0.1", "user": "guest", "password": "guest", "prefetch_count": 1024})

    def test_consumer_adjusts_bulk_size(self):
        """
        Se escolhermos um prefetch menor do que o bulk_size, significa que nosso "bucket"
        nunca vai encher e isso significa que nosso consumer ficará congelado, em um deadlock:
            Ele estará esperando o bucket encher
            E ao mesmo tempo estará o esperando o bucket esvaziar para que possa receber mais mensagens do RabbitMQ


        Vamos setar o bulk_size com sendo min(bulk_size, prefetch_count)
        """
        self.one_route_fixture['options']['bulk_size'] = 2048
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.assertEqual(1024, consumer.bucket.size)

        self.one_route_fixture['options']['bulk_size'] = 4096
        consumer = Consumer(self.one_route_fixture, host="127.0.0.1", username="guest", password="guest", prefetch_count=8192)
        self.assertEqual(4096, consumer.bucket.size)

    def test_consumer_instantiate_using_bucket_class(self):
        class MyBucket(Bucket):
            pass
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters, bucket_class=MyBucket)
        self.assertTrue(isinstance(consumer.bucket, MyBucket))

    def test_consumer_instantiate_correct_size_bucket(self):
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.assertEqual(self.one_route_fixture['options']['bulk_size'], consumer.bucket.size)

    def test_consumer_instantiate_async_queue_default_vhost(self):
        del self.one_route_fixture['options']['vhost']
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        connection_parameters = consumer.queue.connection_parameters

        self.assertTrue(isinstance(consumer.queue, AsyncQueue))
        self.assertEqual("/", connection_parameters['virtualhost'])
        self.assertEqual("127.0.0.1", connection_parameters['host'])
        self.assertEqual("guest", connection_parameters['login'])
        self.assertEqual("guest", connection_parameters['password'])

    def test_consumer_instantiate_async_queue_other_vhost(self):
        self.one_route_fixture["options"]["vhost"] = "fluentd"
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        connection_parameters = consumer.queue.connection_parameters

        self.assertTrue(isinstance(consumer.queue, AsyncQueue))
        self.assertEqual("fluentd", connection_parameters['virtualhost'])

    def test_consumer_instantiate_async_queue_other_vhost_strip_slash(self):
        self.one_route_fixture["options"]["vhost"] = "/fluentd"
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        connection_parameters = consumer.queue.connection_parameters

        self.assertTrue(isinstance(consumer.queue, AsyncQueue))
        self.assertEqual("fluentd", connection_parameters['virtualhost'])

    def test_consumer_instantiate_async_queue_prefetch_count(self):
        self.one_route_fixture["options"]["vhost"] = "/fluentd"
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        connection_parameters = consumer.queue.connection_parameters

        self.assertTrue(isinstance(consumer.queue, AsyncQueue))
        self.assertEqual("fluentd", connection_parameters['virtualhost'])
        self.assertEqual(1024, consumer.queue.prefetch_count)

    def test_consumer_returns_correct_queue_name(self):
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.assertEqual(["/asgard/counts/ok"], consumer.queue_name)

    async def test_on_queue_message_calls_inner_handler(self):
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        result = await consumer.on_queue_message({"key": "value"}, delivery_tag=10, queue=self.queue_mock)

        self.assertEqual((42, {"key": "value"}), result)

    async def test_on_exception_requeue_message(self):
        """
        Confirma que em caso de exceção, será feito `message.reject(requeue=True)`
        """
        @self.app.route(["queue"], options = {Events.ON_EXCEPTION: Actions.REQUEUE})
        async def _handler(messages):
            raise Exception("BOOM!")

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        with self.assertRaises(Exception):
            await consumer.on_queue_message({"key": 42}, delivery_tag=10, queue=self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)

    async def test_on_exception_reject_message(self):
        @self.app.route(["queue"], options={Events.ON_EXCEPTION: Actions.REJECT})
        async def _handler(messages):
            raise Exception("BOOM!")

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        with self.assertRaises(Exception):
            await consumer.on_queue_message({"key": 42}, delivery_tag=10, queue=self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=False)

    async def test_on_exception_ack_message(self):
        @self.app.route(["queue"], options={Events.ON_EXCEPTION: Actions.ACK})
        async def _handler(messages):
            raise Exception("BOOM!")

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)
        with self.assertRaises(Exception):
            await consumer.on_queue_message({"key": 42}, delivery_tag=10, queue=self.queue_mock)

        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)

    async def test_on_success_ack(self):
        @self.app.route(["queue"], options = {Events.ON_SUCCESS: Actions.ACK})
        async def _handler(messages):
            return 42

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        await consumer.on_queue_message({"key": 42}, delivery_tag=10, queue=self.queue_mock)
        self.queue_mock.ack.assert_awaited_with(delivery_tag=10)

    async def test_on_success_reject(self):
        @self.app.route(["queue"], options = {Events.ON_SUCCESS: Actions.REJECT})
        async def _handler(messages):
            return 42

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        await consumer.on_queue_message({"key": 42}, delivery_tag=10, queue=self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=False)

    async def test_on_success_requeue(self):
        @self.app.route(["queue"], options = {Events.ON_SUCCESS: Actions.REQUEUE})
        async def _handler(messages):
            return 42

        route = self.app.routes_registry.amqp_routes[0]
        consumer = Consumer(route, *self.connection_parameters)

        await consumer.on_queue_message({"key": 42}, delivery_tag=10, queue=self.queue_mock)
        self.queue_mock.reject.assert_awaited_with(delivery_tag=10, requeue=True)

    async def test_on_queue_message_auto_ack_on_success(self):
        """
        Se o handler registrado no @app.route() rodar com sucesso,
        devemos fazer o ack da mensagem
        """
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        expected_body = {"key": "value"}
        message_mock = RabbitMQMessage(body=expected_body, delivery_tag=10)

        result = await consumer.on_queue_message(expected_body, delivery_tag=10, queue=self.queue_mock)
        self.assertEqual((42, expected_body), result)
        self.queue_mock.ack.assert_awaited_once_with(delivery_tag=10)
        self.queue_mock.reject.assert_not_awaited()

    async def test_on_exception_default_action_bulk_messages(self):
        """
        Se o handler der raise em qualquer exception, devemos
        dar reject() na mensagem
        """
        async def exception_handler(message):
            return message.do_not_exist

        self.one_route_fixture['handler'] = exception_handler
        self.one_route_fixture['options']['bulk_size'] = 2

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(ack=CoroutineMock(), reject=CoroutineMock())
        with self.assertRaises(AttributeError):
            await consumer.on_queue_message({"key": "value"}, delivery_tag=10, queue=queue_mock)
            await consumer.on_queue_message({"key": "value"}, delivery_tag=11, queue=queue_mock)

        self.assertCountEqual([mock.call(delivery_tag=10, requeue=True), mock.call(delivery_tag=11, requeue=True)], queue_mock.reject.await_args_list)
        queue_mock.ack.assert_not_awaited

    async def test_on_queue_message_precondition_failed_on_ack(self):
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(ack=CoroutineMock(side_effect=AioamqpException))
        with self.assertRaises(AioamqpException):
            await consumer.on_queue_message({"key": "value"}, delivery_tag=10, queue=queue_mock)

    async def test_on_queue_message_bulk_size_one(self):
        class MyBucket(Bucket):
            def pop_all(self):
                return self._items


        handler_mock = CoroutineMock()
        self.one_route_fixture['handler'] = handler_mock
        self.one_route_fixture['options']['bulk_size'] = 1

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters, bucket_class=MyBucket)
        queue_mock = CoroutineMock(ack=CoroutineMock())

        await consumer.on_queue_message({"key": "value"}, delivery_tag=20, queue=queue_mock)
        handler_mock.assert_awaited_once_with(consumer.bucket._items)

        self.assertEqual([mock.call(delivery_tag=20)], queue_mock.ack.await_args_list)
        self.assertEqual(0, queue_mock.reject.call_count)

    async def test_on_queue_message_bulk_size_bigger_that_one(self):
        """
        Confere que o handler real só é chamado quando o bucket atinge o limite máximo de
        tamanho. E que o handler é chamado com a lista de mensagens.
        * Bucket deve estart vazio após o "flush"
        """
        class MyBucket(Bucket):
            def pop_all(self):
                return self._items;


        handler_mock = CoroutineMock()
        self.one_route_fixture['handler'] = handler_mock
        self.one_route_fixture['options']['bulk_size'] = 2

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters, bucket_class=MyBucket)
        queue_mock = CoroutineMock(ack=CoroutineMock())

        await consumer.on_queue_message({"key": "value"}, delivery_tag=10, queue=queue_mock)
        self.assertEqual(0, handler_mock.await_count)

        await consumer.on_queue_message({"key": "value"}, delivery_tag=20, queue=queue_mock)
        handler_mock.assert_awaited_once_with(consumer.bucket._items)

        self.assertCountEqual([mock.call(delivery_tag=10), mock.call(delivery_tag=20)], queue_mock.ack.await_args_list)
        self.assertEqual(0, queue_mock.reject.call_count)

    async def test_on_queue_message_bulk_mixed_ack_and_reject(self):
        async def handler(messages):
            messages[1].reject()
            messages[2].reject()

        self.one_route_fixture['handler'] = handler
        self.one_route_fixture['options']['bulk_size'] = 5

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(ack=CoroutineMock(), reject=CoroutineMock())

        await consumer.on_queue_message({"key": "value"}, delivery_tag=10, queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=11, queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=12, queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=13, queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=14, queue=queue_mock)

        self.assertCountEqual([mock.call(delivery_tag=10), mock.call(delivery_tag=13), mock.call(delivery_tag=14)], queue_mock.ack.await_args_list)
        self.assertCountEqual([mock.call(delivery_tag=11, requeue=True), mock.call(delivery_tag=12, requeue=True)], queue_mock.reject.await_args_list)

    async def test_on_queue_message_bulk_mixed_ack_and_reject_on_success_reject(self):
        self.maxDiff = None
        async def handler(messages):
            messages[1].reject(requeue=True)
            messages[2].reject(requeue=True)

        self.one_route_fixture['handler'] = handler
        self.one_route_fixture['options']['bulk_size'] = 5
        self.one_route_fixture['options'][Events.ON_SUCCESS] = Actions.REJECT

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(ack=CoroutineMock(), reject=CoroutineMock())

        await consumer.on_queue_message({"key": "value"}, delivery_tag=10, queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=11,
                                        queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=12,
                                        queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=13,
                                        queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=14,
                                        queue=queue_mock)

        self.assertCountEqual([mock.call(delivery_tag=10, requeue=False),
                               mock.call(delivery_tag=11, requeue=True),
                               mock.call(delivery_tag=12, requeue=True),
                               mock.call(delivery_tag=13, requeue=False),
                               mock.call(delivery_tag=14, requeue=False)],
                              queue_mock.reject.await_args_list)

    @unittest.skip("")
    async def test_bulk_flushes_on_timeout_even_with_bucket_not_full(self):
        """
        Se nosso bucket não chegar ao total de mensagens do nosso bulk_size, temos
        que fazer flush de tempos em tempos, senão poderemos ficar eternamente com mensagens presas.
        """
        handler_mock = CoroutineMock()
        self.one_route_fixture['handler'] = handler_mock
        self.one_route_fixture['options']['bulk_size'] = 5
        self.one_route_fixture['options']['bulk_flush_interval'] = 3

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(ack=CoroutineMock(), reject=CoroutineMock())

        await consumer.on_queue_message({"key": "value"}, delivery_tag=10, queue=queue_mock)
        await consumer.on_queue_message({"key": "value"}, delivery_tag=11, queue=queue_mock)
        #await consumer.on_queue_message({"key": "value"}, delivery_tag=12, queue=queue_mock)
        #await consumer.on_queue_message({"key": "value"}, delivery_tag=13, queue=queue_mock)
        #await consumer.on_queue_message({"key": "value"}, delivery_tag=14, queue=queue_mock)
        await asyncio.sleep(4)

        #handler_mock.assert_awaited_once
        self.assertEqual(1, handler_mock.await_count)
        self.assertEqual([mock.call(delivery_tag=10), mock.call(delivery_tag=11)], queue_mock.ack.await_args_list)

    @unittest.skip("")
    def test_restart_timeout_on_every_flush(self):
        self.fail()

    @unittest.skip("")
    def test_do_not_flush_if_bucket_is_already_empty_when_timeout_expires(self):
        self.fail()

    async def test_on_message_handle_error_logs_exception(self):
        """
        Logamos a exception lançada pelo handler.
        Aqui o try/except serve apenas para termos uma exception real, com traceback.
        """
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with mock.patch.object(conf, "logger") as logger_mock:
            try:
                1/0
            except Exception as e:
                await consumer.on_message_handle_error(e)
                logger_mock.error.assert_called_with({"exc_message": "division by zero",
                                                      "exc_traceback": mock.ANY,
                                                     })

    async def test_on_connection_error_logs_exception(self):
        """
        Logamos qualquer erro de conexão com o Rabbit, inclusive acesso negado
        """
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with mock.patch.object(conf, "logger") as logger_mock:
            try:
                1/0
            except Exception as e:
                await consumer.on_connection_error(e)
                logger_mock.error.assert_called_with({"exc_message": "division by zero",
                                                      "exc_traceback": mock.ANY,
                                                     })

    async def test_on_queue_error_logs_exception_and_acks_message(self):
        """
        Logamos qualquer erro de parsing/validação de mensagem
        """
        delivery_tag = 42
        body = "not a JSON"
        queue_mock = CoroutineMock(ack=CoroutineMock())

        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with mock.patch.object(conf, "logger") as logger_mock:
            await consumer.on_queue_error(body, delivery_tag, "Error: not a JSON", queue_mock)
            logger_mock.error.assert_called_with({"exception": "Error: not a JSON",
                                                  "original_msg": body,
                                                  "parse-error": True})
            queue_mock.ack.assert_awaited_once_with(delivery_tag=delivery_tag)

    def test_return_correct_queue_name(self):
        """
        consumer.quene_name deve retornar o nome da fila que está sendo consumida.
        """
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        self.assertEquals(self.one_route_fixture['routes'], consumer.queue_name)

    async def test_consume_all_queues(self):
        """
        """
        self.one_route_fixture['routes'] = ["asgard/counts", "asgard/counts/errors"]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(consume=CoroutineMock())
        await consumer.consume_all_queues(queue_mock)
        self.assertEqual(2, queue_mock.consume.await_count)
        self.assertEqual([mock.call(queue_name="asgard/counts"), mock.call(queue_name="asgard/counts/errors")], queue_mock.consume.await_args_list)

    def test_start_calls_connect_and_consume_for_each_queue(self):
        self.one_route_fixture['routes'] = ["asgard/counts", "asgard/counts/errors"]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        queue_mock = CoroutineMock(consume=CoroutineMock(), connect=CoroutineMock(), is_connected=False)
        loop = asyncio.get_event_loop()
        consumer.queue = queue_mock

        with asynctest.patch.object(consumer, 'keep_runnig', side_effect=[True, False]) as keep_running_mock:
            loop.run_until_complete(consumer.start())

        self.assertEqual(1, queue_mock.connect.await_count)
        self.assertEqual(2, queue_mock.consume.await_count)
        self.assertEqual([mock.call(queue_name="asgard/counts"), mock.call(queue_name="asgard/counts/errors")], queue_mock.consume.await_args_list)

    def test_start_reconnects_if_connectaion_failed(self):
        self.one_route_fixture['routes'] = ["asgard/counts", "asgard/counts/errors"]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with unittest.mock.patch.object(consumer, 'keep_runnig', side_effect=[True, True, False]), \
                asynctest.patch.object(asyncio, 'sleep') as sleep_mock:
            is_connected_mock = mock.PropertyMock(side_effect=[False, False, True])
            queue_mock = CoroutineMock(consume=CoroutineMock(), connect=CoroutineMock(side_effect=[AioamqpException, True]))
            type(queue_mock).is_connected = is_connected_mock
            loop = asyncio.get_event_loop()
            consumer.queue = queue_mock
            loop.run_until_complete(consumer.start())
            self.assertEqual(1, queue_mock.connect.await_count)
            self.assertEqual(2, queue_mock.consume.await_count)
            self.assertEqual([mock.call(queue_name="asgard/counts"), mock.call(queue_name="asgard/counts/errors")], queue_mock.consume.await_args_list)
            self.assertEqual(2, sleep_mock.await_count)

    def test_start_always_calls_sleep(self):
        """
        Regression:
            O sleep deve ser chamado *sempre*, e não apenas quando há tentativa de conexão.
            Aqui, tentamos reconectar apenas uma vez, mas mesmo assim o sleep é chamado 3x, pois o loop principal
            roda 3x.
        """
        self.one_route_fixture['route'] = ["asgard/counts", "asgard/counts/errors"]
        consumer = Consumer(self.one_route_fixture, *self.connection_parameters)
        with unittest.mock.patch.object(consumer, 'keep_runnig', side_effect=[True, True, True, False]), \
                asynctest.patch.object(asyncio, 'sleep') as sleep_mock:
            is_connected_mock = mock.PropertyMock(side_effect=[False, True, True, True])
            queue_mock = CoroutineMock(consume=CoroutineMock(), connect=CoroutineMock())
            type(queue_mock).is_connected = is_connected_mock
            loop = asyncio.get_event_loop()
            consumer.queue = queue_mock
            loop.run_until_complete(consumer.start())
            self.assertEqual(3, sleep_mock.await_count)

