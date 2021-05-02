from typing import Callable, TypeVar, Generic, Optional

from aioamqp.channel import Channel
from aioamqp.envelope import Envelope
from aioamqp.properties import Properties

from asyncworker.easyqueue.connection import AMQPConnection
from asyncworker.easyqueue.exceptions import UndecodableMessageException

T = TypeVar("T")


class AMQPMessage(Generic[T]):
    __slots__ = (
        "connection",
        "channel",
        "queue_name",
        "serialized_data",
        "delivery_tag",
        "_envelope",
        "_properties",
        "_deserialization_method",
        "_deserialized_data",
        "_queue",
    )

    def __init__(
        self,
        connection: AMQPConnection,
        channel: Channel,
        queue_name: str,
        serialized_data: bytes,
        delivery_tag: int,
        envelope: Envelope,
        properties: Properties,
        deserialization_method: Callable[[bytes], T],
        queue,
    ) -> None:
        self.queue_name = queue_name
        self.serialized_data = serialized_data
        self.delivery_tag = delivery_tag
        self.connection = connection
        self.channel = channel
        self._envelope = envelope
        self._properties = properties
        self._deserialization_method = deserialization_method

        self._deserialized_data: Optional[T] = None
        self._queue = queue

    @property
    def deserialized_data(self) -> T:
        if self._deserialized_data:
            return self._deserialized_data
        try:
            self._deserialized_data = self._deserialization_method(
                self.serialized_data
            )
        except ValueError as e:
            raise UndecodableMessageException(
                "msg couldn't be decoded as JSON"
            ) from e
        return self._deserialized_data

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            if attr.startswith("__"):
                continue
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    async def ack(self):
        return await self.channel.basic_client_ack(self.delivery_tag)

    async def reject(self, requeue=False):
        return await self.channel.basic_reject(
            delivery_tag=self.delivery_tag, requeue=requeue
        )
