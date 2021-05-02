import abc
import asyncio
from collections import UserList


class Freezable(metaclass=abc.ABCMeta):
    def __init__(self):
        self._frozen = False

    @property
    def frozen(self) -> bool:
        return self._frozen

    async def freeze(self):
        self._frozen = True


class Signal(UserList, asyncio.Event):
    """
    Coroutine-based signal implementation tha behaves as an `asyncio.Event`.

    To connect a callback to a signal, use any list method.

    Signals are fired using the send() coroutine, which takes named
    arguments.
    """

    def __init__(self, owner: Freezable) -> None:
        UserList.__init__(self)
        asyncio.Event.__init__(self)
        self._owner = owner
        self.frozen = False

    def __repr__(self):
        return "<Signal owner={}, frozen={}, {!r}>".format(
            self._owner, self.frozen, list(self)
        )

    async def send(self, *args, **kwargs):
        """
        Sends data to all registered receivers.
        """
        if self.frozen:
            raise RuntimeError("Cannot send on frozen signal.")

        for receiver in self:
            await receiver(*args, **kwargs)

        self.frozen = True
        await self._owner.freeze()
        self.set()
