import asyncio
from typing import Callable, Union, Coroutine, Optional

import aioamqp
from aioamqp import AmqpProtocol
from aioamqp.channel import Channel

from asyncworker import metrics

OnErrorCallback = Union[
    None, Callable[[Exception], None], Callable[[Exception], Coroutine]
]


class AMQPConnection:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        heartbeat: int = 60,
        virtual_host: str = "/",
        loop: asyncio.AbstractEventLoop = None,
        on_error: OnErrorCallback = None,
    ) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self.heartbeat = heartbeat
        self.loop = loop
        self._on_error = on_error

        self._connection_lock = asyncio.Lock()

        self.channel: Channel = None
        self._transport: Optional[asyncio.BaseTransport] = None
        self._protocol: AmqpProtocol = None

    @property
    def connection_parameters(self):
        return {
            "host": self.host,
            "login": self.username,
            "password": self.password,
            "virtualhost": self.virtual_host,
            "loop": self.loop,
            "on_error": self._on_error,
            "heartbeat": self.heartbeat,
        }

    @property
    def is_connected(self) -> bool:
        if self.channel is None:
            return False

        return self.channel and self.channel.is_open

    async def close(self) -> None:
        if not self.is_connected:
            return None

        await self._protocol.close()
        self._transport.close()  # type: ignore
        metrics.active_connections.dec()

    async def _connect(self) -> None:
        async with self._connection_lock:
            if self.is_connected:
                return

            conn = await aioamqp.connect(**self.connection_parameters)
            self._transport, self._protocol = conn
            self.channel = await self._protocol.channel()
            metrics.active_connections.inc()
