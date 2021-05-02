import asyncio
from typing import Callable, Union, Coroutine, Optional

import aioamqp
from aioamqp import AmqpProtocol
from aioamqp.channel import Channel
from aioamqp.exceptions import AioamqpException
from aioamqp.protocol import OPEN

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
        procotol_ok = self._protocol and self._protocol.state == OPEN
        return procotol_ok

    def has_channel_ready(self):
        channel_ok = self.channel and self.channel.is_open
        return channel_ok

    async def close(self) -> None:
        if not self.is_connected:
            return None

        await self._protocol.close()
        self._transport.close()  # type: ignore

    async def _connect(self) -> None:
        async with self._connection_lock:
            if self.is_connected and self.has_channel_ready():
                return

            try:
                if self._protocol:
                    self.channel = await self._protocol.channel()
                    return
            except AioamqpException as e:
                # Se não conseguirmos pegar um channel novo
                # a conexão atual deve mesmo ser renovada e isso
                # será feito logo abaixo.
                pass

            conn = await aioamqp.connect(**self.connection_parameters)
            self._transport, self._protocol = conn
            self.channel = await self._protocol.channel()
