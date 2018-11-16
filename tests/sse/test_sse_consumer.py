from asynctest import TestCase
from asynctest.mock import CoroutineMock
import asynctest
import aiohttp
from urllib.parse import urljoin

from aioresponses import aioresponses

from asyncworker.sse.consumer import SSEConsumer
from asyncworker.bucket import Bucket
from tests.utils import get_fixture


async def _handler(message):
    return (42, message[0].body)

class SSEConsumerTest(TestCase):


    def total_loops(self, n):
        return [True] * n + [False]

    async def setUp(self):
        self.one_route_fixture = {
            "routes": ["/asgard/counts/ok"],
            "handler": _handler,
            "options": {
                "vhost": "/",
                "bulk_size": 1,
                "bulk_flush_interval": 60,
            }
        }
        self.consumer_params = ("http://localhost:8080/v2/events", "guest", "guest")
        self.consumer = SSEConsumer(self.one_route_fixture, *self.consumer_params)
        self.consumer.interval = 0

    async def test_new_consumer_instance(self):
        consumer = SSEConsumer(self.one_route_fixture, *self.consumer_params)
        self.assertEqual(consumer.url, self.consumer_params[0])
        self.assertEqual(consumer.route_info, self.one_route_fixture)
        self.assertEqual(consumer._handler, self.one_route_fixture['handler'])
        self.assertEqual(self.consumer_params[1], consumer.username)
        self.assertEqual(self.consumer_params[2], consumer.password)
        
        final_route = urljoin(self.consumer_params[0], self.one_route_fixture['routes'][0])
        self.assertEqual([final_route], consumer.routes)

    def test_new_consumer_instance_multiple_routes(self):
        self.one_route_fixture['routes'].append("/v2/events")

        consumer = SSEConsumer(self.one_route_fixture, *self.consumer_params)
        self.assertEqual(consumer.url, self.consumer_params[0])
        self.assertEqual(consumer.route_info, self.one_route_fixture)
        self.assertEqual(consumer._handler, self.one_route_fixture['handler'])
        
        expected_routes = [
            urljoin(self.consumer_params[0], self.one_route_fixture['routes'][0]),
            urljoin(self.consumer_params[0], self.one_route_fixture['routes'][1]),
        ]
        self.assertEqual(expected_routes, consumer.routes)

    @asynctest.skip("aiohttp não está seguindo esse redirect do aioresponses")
    async def test_follow_redirect(self):
        content = open("./tests/fixtures/sse/single-event.txt").read()

        with asynctest.patch.object(consumer, 'keep_runnig', side_effect=[True, False]), \
                asynctest.patch.object(consumer, "on_event") as on_event_mock:
            with aioresponses() as m:
                m.get("http://localhost:8081/v2/events", status=301, headers={"Location": "http://localhost:8080/v2/events"})
                m.get("http://localhost:8080/v2/events", status=200, body=content)
                __import__('ipdb').set_trace()
                await self.consumer.start()
                args_list = on_event_mock.await_args_list
                self.assertEqual([asynctest.mock.call(b'event_stream_attached',
                                                      b'{"remoteAddress":"172.18.0.1","eventType":"event_stream_attached","timestamp":"2018-09-03T18:03:45.685Z"}')], args_list)

    async def test_call_on_event_when_sse_event_is_found(self):
        """
        A cada par de linhas:
            event: ...
            data: ...
        Chamamos o método `on_event()`
        """
        content = get_fixture("sse/single-event.txt")

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=[True, False]), \
                asynctest.patch.object(self.consumer, "on_event") as on_event_mock:
            with aioresponses() as m:
                m.get("http://localhost:8080/v2/events", status=200, body=content)
                await self.consumer.start()
                args_list = on_event_mock.await_args_list
                self.assertEqual([asynctest.mock.call(b'event_stream_attached',
                                                      b'{"remoteAddress":"172.18.0.1","eventType":"event_stream_attached","timestamp":"2018-09-03T18:03:45.685Z"}')], args_list)

    async def test_call_on_event_ignore_blank_lines(self):
        content = get_fixture("sse/multi-event-blanklines-in-between.txt")

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=[True, False]), \
                asynctest.patch.object(self.consumer, "on_event") as on_event_mock:
            with aioresponses() as m:
                m.get("http://localhost:8080/v2/events", status=200, body=content)
                await self.consumer.start()
                self.assertEqual(4, on_event_mock.await_count)
                args_list = on_event_mock.await_args_list

                event_1 = (
                    b"group_change_success",
                    b'{"groupId":"/asgard-dev","version":"2018-09-04T12:58:57.000Z","eventType":"group_change_success","timestamp":"2018-09-04T12:58:57.072Z"}'
                )

                event_2 =(
                    b"api_post_event",
                    b'{"clientIp":"172.18.0.1","uri":"/v2/apps//asgard-dev/bla","appDefinition":{"id":"/asgard-dev/bla","cmd":"sleep 1000","args":null,"user":null,"env":{},"instances":0,"cpus":1,"mem":128,"disk":0,"gpus":0,"executor":"","constraints":[],"uris":[],"fetch":[],"storeUrls":[],"backoffSeconds":1,"backoffFactor":1.15,"maxLaunchDelaySeconds":3600,"container":{"type":"DOCKER","volumes":[],"docker":{"image":"alpine","network":"BRIDGE","portMappings":[],"privileged":false,"parameters":[],"forcePullImage":false}},"healthChecks":[],"readinessChecks":[],"dependencies":[],"upgradeStrategy":{"minimumHealthCapacity":1,"maximumOverCapacity":1},"labels":{},"ipAddress":null,"version":"2018-09-04T12:58:57.000Z","residency":null,"secrets":{},"taskKillGracePeriodSeconds":null,"unreachableStrategy":{"inactiveAfterSeconds":0,"expungeAfterSeconds":0},"killSelection":"YOUNGEST_FIRST","ports":[10006],"portDefinitions":[{"port":10006,"protocol":"tcp","name":"default","labels":{}}],"requirePorts":false,"versionInfo":{"lastScalingAt":"2018-09-04T12:58:57.000Z","lastConfigChangeAt":"2018-09-04T12:56:56.861Z"}},"eventType":"api_post_event","timestamp":"2018-09-04T12:58:57.073Z"}'
                )

                event_3 =(
                    b"status_update_event",
                    b'{"slaveId":"40cf614e-b392-4d31-9230-090ca3c7aa83-S0","taskId":"asgard-dev_bla.0139427f-b042-11e8-9638-0242ac12001f","taskStatus":"TASK_KILLED","message":"Container exited with status 137","appId":"/asgard-dev/bla","host":"172.18.0.51","ipAddresses":[{"ipAddress":"172.17.0.4","protocol":"IPv4"}],"ports":[30989],"version":"2018-09-04T12:56:56.861Z","eventType":"status_update_event","timestamp":"2018-09-04T12:59:57.728Z"}'    
                )

                event_4 =(
                    b"instance_changed_event",
                    b'{"instanceId":"asgard-dev_bla.marathon-0139427f-b042-11e8-9638-0242ac12001f","condition":"Killed","runSpecId":"/asgard-dev/bla","agentId":"40cf614e-b392-4d31-9230-090ca3c7aa83-S0","host":"172.18.0.51","runSpecVersion":"2018-09-04T12:56:56.861Z","timestamp":"2018-09-04T12:59:57.739Z","eventType":"instance_changed_event"}'
                )

                self.assertEqual([
                    asynctest.mock.call(*event_1),
                    asynctest.mock.call(*event_2),
                    asynctest.mock.call(*event_3),
                    asynctest.mock.call(*event_4),
                ], args_list)


    async def test_reconnect_if_disconnected(self):
        session_mock = CoroutineMock(get=CoroutineMock(side_effect=["", aiohttp.ClientError(), aiohttp.ClientError()]))
        self.consumer.session = session_mock

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=[True, True, True, False]), \
                asynctest.patch.object(self.consumer, "_consume_events", side_effect=CoroutineMock()) as consume_events_mock:
            await self.consumer.start()
            self.assertEqual(1, consume_events_mock.await_count)
            self.assertEqual(3, session_mock.get.call_count)
            self.assertEqual(1, session_mock.get.await_count)
                
    async def test_consume_again_if_reconnected(self):
        session_mock = CoroutineMock(get=CoroutineMock(side_effect=["", aiohttp.ClientError(), ""]))
        self.consumer.session = session_mock

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=[True, True, True, False]), \
                asynctest.patch.object(self.consumer, "_consume_events", side_effect=CoroutineMock()) as consume_events_mock:
            await self.consumer.start()
            self.assertEqual(2, consume_events_mock.await_count)
            self.assertEqual(3, session_mock.get.call_count)
            self.assertEqual(2, session_mock.get.await_count)

    async def test_call_on_connection_error(self):
        """
        Call on_connection_error when an aiohttp.ClientError is raised
        """
        session_mock = CoroutineMock(get=CoroutineMock(side_effect=[aiohttp.ClientError()]))
        self.consumer.session = session_mock

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=self.total_loops(1)), \
                asynctest.patch.object(self.consumer, "on_connection_error", side_effect=CoroutineMock()) as on_connection_error_mock:
            await self.consumer.start()
            self.assertEqual(1, on_connection_error_mock.await_count)

    async def test_call_on_exception(self):
        """
        Call on_exceptin when an unhandled exception is raised
        """

        content = get_fixture("sse/single-event.txt")

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=self.total_loops(1)), \
                asynctest.patch.object(self.consumer, "on_event", side_effect=Exception()), \
                asynctest.patch.object(self.consumer, "on_exception", side_effect=CoroutineMock()) as on_exception_mock:
            with aioresponses() as m:
                m.get("http://localhost:8080/v2/events", status=200, body=content)
                await self.consumer.start()
                self.assertEqual(1, on_exception_mock.await_count)

    async def test_reconect_if_unhandled_reconnected(self):
        session_mock = CoroutineMock(get=CoroutineMock(side_effect=["", Exception()]))
        self.consumer.session = session_mock

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=[True, True, False]), \
                asynctest.patch.object(self.consumer, "_consume_events", side_effect=CoroutineMock()) as consume_events_mock:
            await self.consumer.start()
            self.assertEqual(1, consume_events_mock.await_count)
            self.assertEqual(2, session_mock.get.call_count)
            self.assertEqual(1, session_mock.get.await_count)

    @asynctest.skip("Decidir o que fazer...")
    async def test_flush_bucket_on_connection_error(self):
        """
        Sempre que o stream acabar, ou formos desconectados
        temos que fazer flush do bucket.
        """
        self.fail()

    async def test_call_on_connect_callback(self):
        session_mock = CoroutineMock(get=CoroutineMock())
        self.consumer.session = session_mock

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=self.total_loops(1)), \
                asynctest.patch.object(self.consumer, "on_connection", side_effect=CoroutineMock()) as on_connection_mock:
            await self.consumer.start()
            self.assertEqual(1, on_connection_mock.call_count)
            self.assertEqual(1, on_connection_mock.await_count)

    async def test_do_not_call_on_connect_callback_if_connection_error(self):
        session_mock = CoroutineMock(get=CoroutineMock(side_effect=[aiohttp.ClientError()]))
        self.consumer.session = session_mock

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=self.total_loops(1)), \
                asynctest.patch.object(self.consumer, "on_connection", side_effect=CoroutineMock()) as on_connection_mock:
            await self.consumer.start()
            self.assertEqual(0, on_connection_mock.call_count)
            self.assertEqual(0, on_connection_mock.await_count)

    async def test_call_on_connect_callback_on_reconnect(self):
        session_mock = CoroutineMock(get=CoroutineMock(side_effect=["", aiohttp.ClientError(), ""]))
        self.consumer.session = session_mock

        with asynctest.patch.object(self.consumer, 'keep_runnig', side_effect=self.total_loops(3)), \
                asynctest.patch.object(self.consumer, "on_connection", side_effect=CoroutineMock()) as on_connection_mock:
            await self.consumer.start()
            self.assertEqual(2, on_connection_mock.call_count)
            self.assertEqual(2, on_connection_mock.await_count)

class SSEOnEventCallbackTest(TestCase):

    async def setUp(self):
        self.one_route_fixture = {
            "routes": ["/asgard/counts/ok"],
            "handler": _handler,
            "options": {
                "vhost": "/",
                "bulk_size": 1,
                "bulk_flush_interval": 60,
            }
        }
        self.consumer_params = ("http://localhost:8080/v2/events", "guest", "guest")
        self.consumer = SSEConsumer(self.one_route_fixture, *self.consumer_params)

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

        consumer = SSEConsumer(self.one_route_fixture, *(self.consumer_params + (MyBucket,)))

        result = await consumer.on_event(b"deployment_info", b'{"key": "value"}')
        self.assertEqual(0, handler_mock.await_count)

        result = await consumer.on_event(b"deployment_info", b'{"key": "value"}')
        handler_mock.assert_awaited_once_with(consumer.bucket._items)

    async def test_consumer_instantiate_using_bucket_class(self):
        class MyBucket(Bucket):
            pass
        consumer = SSEConsumer(self.one_route_fixture, *(self.consumer_params + (MyBucket,)))
        self.assertTrue(isinstance(consumer.bucket, MyBucket))

    async def test_consumer_instantiate_correct_size_bucket(self):
        self.one_route_fixture['options']['bulk_size'] = 42
        consumer = SSEConsumer(self.one_route_fixture, *self.consumer_params)
        self.assertEqual(self.one_route_fixture['options']['bulk_size'], consumer.bucket.size)

    async def test_on_event_calls_inner_handler(self):
        consumer = SSEConsumer(self.one_route_fixture, *self.consumer_params)
        result = await consumer.on_event(b"deployment_info", b'{"key": "value"}')

        self.assertEqual((42, {"key": "value"}), result)
