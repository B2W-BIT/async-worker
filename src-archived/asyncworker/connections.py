import abc
import collections
from collections.abc import KeysView, ValuesView
from typing import (
    Optional,
    Union,
    List,
    Dict,
    Any,
    Type,
    Mapping,
    Iterable,
    Counter,
    ItemsView,
)

from pydantic import BaseModel, validator

from asyncworker.conf import settings
from asyncworker.easyqueue.queue import JsonQueue
from asyncworker.exceptions import InvalidConnection
from asyncworker.options import RouteTypes
from asyncworker.signals.base import Freezable


class Connection(BaseModel, abc.ABC):
    """
    Common ancestral for all Connection classes that auto generates a
    connection name and is responsible for keeping track of new connections on
    the ConnectionsMapping
    """

    route_type: RouteTypes
    name: Optional[str] = None


class ConnectionsMapping(Mapping[str, Connection], Freezable):
    """
    A mapping (Connection.name->Connection) of all available connections that
    also keeps a counter for each connection type
    """

    def __getitem__(self, k: str) -> Connection:
        return self._data[k]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __init__(self) -> None:
        Freezable.__init__(self)
        self._data: Dict[str, Connection] = {}
        self.counter: Counter[Type[Connection]] = collections.Counter()

    def __contains__(self, item):
        if isinstance(item, Connection):
            return item in self.values()
        return super(ConnectionsMapping, self).__contains__(item)

    def __setitem__(self, key: str, value: Connection) -> None:
        if self.frozen:
            raise RuntimeError(
                "You shouldn't change the state of ConnectionsMapping "
                "after App startup"
            )

        if key is None:
            key = id(value)

        if key in self:
            raise InvalidConnection(
                f"Invalid connection: `{value}`. "
                f"The name `{key}` already exists in {self.__class__.__name__}"
            )
        self._data[key] = value
        self.counter[value.__class__] += 1

    def __delitem__(self, key: str) -> None:
        if self.frozen:
            raise RuntimeError(
                "You shouldn't change the state of ConnectionsMapping "
                "after App startup"
            )
        del self._data[key]

    def add(self, connections: Iterable[Connection]) -> None:
        for conn in connections:
            self[conn.name] = conn  # type: ignore

    def with_type(self, route_type: RouteTypes) -> List["Connection"]:
        # todo: manter uma segunda estrutura de dados ou aceitar O(n) sempre que chamado?
        return [conn for conn in self.values() if conn.route_type == route_type]


_TYPE_COUNTER: Counter[Type[Connection]] = collections.Counter()

Message = Union[List, Dict]


class AMQPConnection(Connection):
    hostname: str
    username: str
    password: str
    route_type = RouteTypes.AMQP_RABBITMQ
    prefetch: int = settings.AMQP_DEFAULT_PREFETCH_COUNT
    heartbeat: int = settings.AMQP_DEFAULT_HEARTBEAT
    name: Optional[str] = None
    connections: Dict[str, JsonQueue] = {}

    class Config:
        arbitrary_types_allowed = True

    @validator("connections", pre=True, always=True, check_fields=False)
    def set_connections(cls, v):
        return v or {}

    def __len__(self) -> int:
        return len(self.connections)

    def __iter__(self):
        return iter(self.connections)

    def __getitem__(self, key: str) -> JsonQueue:
        """
        Gets a JsonQueue instance for a given virtual host

        :param key: The virtual host of the connection
        :return: An instance of the connection
        """
        try:
            return self.connections[key]
        except KeyError:
            conn: JsonQueue = JsonQueue(
                host=self.hostname,
                username=self.username,
                password=self.password,
                virtual_host=key,
            )
            self.connections[key] = conn
            return conn

    def keys(self):
        return KeysView(self)

    def items(self):
        return ItemsView(self)

    def values(self):
        return ValuesView(self)

    def register(self, queue: JsonQueue) -> None:
        self.connections[queue.virtual_host] = queue

    async def put(
        self,
        routing_key: str,
        data: Any = None,
        serialized_data: Union[str, bytes] = None,
        exchange: str = "",
        vhost: str = settings.AMQP_DEFAULT_VHOST,
        properties: dict = None,
        mandatory: bool = False,
        immediate: bool = False,
    ):
        conn = self[vhost]
        return await conn.put(
            routing_key=routing_key,
            data=data,
            serialized_data=serialized_data,
            exchange=exchange,
            properties=properties,
            mandatory=mandatory,
            immediate=immediate,
        )
