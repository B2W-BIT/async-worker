import abc
import asyncio
import json
import logging
import traceback
from asyncio import Task, AbstractEventLoop
from enum import Enum, auto
from functools import wraps
from typing import (
    Dict,
    Any,
    Callable,
    Coroutine,
    TypeVar,
    Optional,
    Generic,
    Type,
    Union,
)

from aioamqp.channel import Channel
from aioamqp.envelope import Envelope
from aioamqp.properties import Properties

from asyncworker.easyqueue.connection import AMQPConnection
from asyncworker.easyqueue.exceptions import UndecodableMessageException
from asyncworker.easyqueue.message import AMQPMessage


class DeliveryModes:
    NON_PERSISTENT = 1
    PERSISTENT = 2


class ConnType(Enum):
    CONSUME = auto()
    WRITE = auto()


class BaseQueue(metaclass=abc.ABCMeta):
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        virtual_host: str = "/",
        heartbeat: int = 60,
    ) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self.heartbeat = heartbeat

    @abc.abstractmethod
    def serialize(self, body: Any, **kwargs) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def deserialize(self, body: bytes) -> Any:
        raise NotImplementedError

    def _parse_message(self, content) -> Dict[str, Any]:
        """
        Gets the raw message body as an input, handles deserialization and
        outputs
        :param content: The raw message body
        """
        try:
            return self.deserialize(content)
        except TypeError:
            return self.deserialize(content.decode())
        except json.decoder.JSONDecodeError as e:
            raise UndecodableMessageException(
                '"{content}" can\'t be decoded as JSON'.format(content=content)
            )


class BaseJsonQueue(BaseQueue):
    content_type = "application/json"

    def serialize(self, body: Any, **kwargs) -> str:
        return json.dumps(body, **kwargs)

    def deserialize(self, body: bytes) -> Any:
        return json.loads(body.decode())


def _ensure_conn_is_ready(conn_type: ConnType):
    def _ensure_connected(coro: Callable[..., Coroutine]):
        @wraps(coro)
        async def wrapper(self: "JsonQueue", *args, **kwargs):
            conn = self.conn_types[conn_type]
            retries = 0
            while self.is_running and not conn.has_channel_ready():
                try:
                    await conn._connect()
                    break
                except Exception as e:
                    await asyncio.sleep(self.seconds_between_conn_retry)
                    retries += 1
                    if self.connection_fail_callback:
                        await self.connection_fail_callback(e, retries)
                    if self.logger:
                        self.logger.error(
                            {
                                "event": "reconnect-failure",
                                "retry_count": retries,
                                "exc_traceback": traceback.format_tb(
                                    e.__traceback__
                                ),
                            }
                        )
            return await coro(self, *args, **kwargs)

        return wrapper

    return _ensure_connected


T = TypeVar("T")


class _ConsumptionHandler:
    def __init__(
        self,
        delegate: "QueueConsumerDelegate",
        queue: "JsonQueue",
        queue_name: str,
    ) -> None:
        self.delegate = delegate
        self.queue = queue
        self.loop = queue.loop
        self.queue_name = queue_name
        self.consumer_tag: Optional[str] = None

    async def _handle_callback(self, callback, **kwargs):
        """
        Chains the callback coroutine into a try/except and calls
        `on_message_handle_error` in case of failure, avoiding unhandled
        exceptions.

        :param callback:
        :param kwargs:
        :return:
        """
        try:
            return await callback(**kwargs)
        except Exception as e:
            return await self.delegate.on_message_handle_error(
                handler_error=e, **kwargs
            )

    async def handle_message(
        self,
        channel: Channel,
        body: bytes,
        envelope: Envelope,
        properties: Properties,
    ) -> Task:
        msg = AMQPMessage(
            connection=self.queue.connection,
            channel=channel,
            queue=self.queue,
            envelope=envelope,
            properties=properties,
            delivery_tag=envelope.delivery_tag,
            deserialization_method=self.queue.deserialize,
            queue_name=self.queue_name,
            serialized_data=body,
        )

        callback = self._handle_callback(
            self.delegate.on_queue_message, msg=msg  # type: ignore
        )
        return self.loop.create_task(callback)


class JsonQueue(BaseQueue, Generic[T]):
    _transport: Optional[asyncio.BaseTransport]

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        delegate_class: Type["QueueConsumerDelegate"] = None,
        delegate: Optional["QueueConsumerDelegate"] = None,
        virtual_host: str = "/",
        heartbeat: int = 60,
        prefetch_count: int = 100,
        loop: AbstractEventLoop = None,
        seconds_between_conn_retry: int = 1,
        logger: logging.Logger = None,
        connection_fail_callback: Optional[
            Callable[[Exception, int], Coroutine]
        ] = None,
    ) -> None:
        super().__init__(host, username, password, virtual_host, heartbeat)

        self.loop = loop or asyncio.get_event_loop()

        if delegate is not None and delegate_class is not None:
            raise ValueError("Cant provide both delegate and delegate_class")

        if delegate_class is not None:
            self.delegate = delegate_class()
        else:
            self.delegate = delegate  # type: ignore

        self.prefetch_count = prefetch_count

        on_error = self.delegate.on_connection_error if self.delegate else None

        self.connection = AMQPConnection(
            host=host,
            username=username,
            password=password,
            virtual_host=virtual_host,
            heartbeat=heartbeat,
            on_error=on_error,
            loop=loop,
        )

        self._write_connection = AMQPConnection(
            host=host,
            username=username,
            password=password,
            virtual_host=virtual_host,
            heartbeat=heartbeat,
            on_error=on_error,
            loop=loop,
        )

        self.conn_types = {
            ConnType.CONSUME: self.connection,
            ConnType.WRITE: self._write_connection,
        }

        self.seconds_between_conn_retry = seconds_between_conn_retry
        self.is_running = True
        self.logger = logger
        self.connection_fail_callback = connection_fail_callback

    def serialize(self, body: T, **kwargs) -> str:
        return json.dumps(body, **kwargs)

    def deserialize(self, body: bytes) -> T:
        return json.loads(body.decode())

    def conn_for(self, type: ConnType) -> AMQPConnection:
        return self.conn_types[type]

    @_ensure_conn_is_ready(ConnType.WRITE)
    async def put(
        self,
        routing_key: str,
        data: Any = None,
        serialized_data: Union[str, bytes] = "",
        exchange: str = "",
        properties: dict = None,
        mandatory: bool = False,
        immediate: bool = False,
    ):
        """
        :param data: A serializable data that should be serialized before
        publishing
        :param serialized_data: A payload to be published as is
        :param exchange: The exchange to publish the message
        :param routing_key: The routing key to publish the message
        """
        if data and serialized_data:
            raise ValueError("Only one of data or json should be specified")

        if data:
            serialized_data = self.serialize(data, ensure_ascii=False)

        if not isinstance(serialized_data, bytes):
            serialized_data = serialized_data.encode()

        return await self._write_connection.channel.publish(
            payload=serialized_data,
            exchange_name=exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )

    @_ensure_conn_is_ready(ConnType.CONSUME)
    async def consume(
        self,
        queue_name: str,
        delegate: "QueueConsumerDelegate",
        consumer_name: str = "",
    ) -> str:
        """
        Connects the client if needed and starts queue consumption, sending
        `on_before_start_consumption` and `on_consumption_start` notifications
        to the delegate object

        :param queue_name: queue name to consume from
        :param consumer_name: An optional name to be used as a consumer
        identifier. If one isn't provided, a random one is generated by the
        broker
        :return: The consumer tag. Useful for cancelling/stopping consumption
        """
        # todo: Implement a consumer tag generator
        handler = _ConsumptionHandler(
            delegate=delegate, queue=self, queue_name=queue_name
        )

        await delegate.on_before_start_consumption(
            queue_name=queue_name, queue=self
        )
        await self.connection.channel.basic_qos(
            prefetch_count=self.prefetch_count,
            prefetch_size=0,
            connection_global=False,
        )
        tag = await self.connection.channel.basic_consume(
            callback=handler.handle_message,
            consumer_tag=consumer_name,
            queue_name=queue_name,
        )
        consumer_tag = tag["consumer_tag"]
        await delegate.on_consumption_start(
            consumer_tag=consumer_tag, queue=self
        )
        handler.consumer_tag = consumer_tag
        return consumer_tag


class QueueConsumerDelegate(metaclass=abc.ABCMeta):
    async def on_before_start_consumption(
        self, queue_name: str, queue: JsonQueue
    ):
        """
        Coroutine called before queue consumption starts. May be overwritten to
        implement further custom initialization.

        :param queue_name: Queue name that will be consumed
        :type queue_name: str
        :param queue: AsynQueue instanced
        :type queue: JsonQueue
        """
        pass

    async def on_consumption_start(self, consumer_tag: str, queue: JsonQueue):
        """
        Coroutine called once consumption started.
        """

    @abc.abstractmethod
    async def on_queue_message(self, msg: AMQPMessage[Any]):
        """
        Callback called every time that a new, valid and deserialized message
        is ready to be handled.

        :param msg: the consumed message
        """
        raise NotImplementedError

    async def on_message_handle_error(self, handler_error: Exception, **kwargs):
        """
        Callback called when an uncaught exception was raised during message
        handling stage.

        :param handler_error: The exception that triggered
        :param kwargs: arguments used to call the coroutine that handled
        the message
        :return:
        """
        pass

    async def on_connection_error(self, exception: Exception):
        """
        Called when the connection fails
        """
        pass
