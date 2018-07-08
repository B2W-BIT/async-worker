from time import time as now
from typing import Callable, Coroutine, Type, Optional, Any


Traceback = Any  # fixme: Substituir pelo tipo correto de traceback
TimeitCallback = Callable[
    [
        str,
        float,
        Optional[Type[Exception]],
        Optional[Exception],
        Optional[Traceback]
    ],
    Coroutine
]


class Timeit:
    def __init__(self,
                 name: str,
                 callback: TimeitCallback):
        self.name = name
        self.callback = callback
        self.start: float = None
        self.finish: float = None

    @property
    def time_delta(self) -> float:
        return self.finish - self.start

    async def __aenter__(self):
        self.start = now()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.finish = now()
        if exc_type:
            await self.callback(
                self.name,
                self.time_delta,
                exc_type,
                exc_val,
                exc_tb
            )
        else:
            await self.callback(self.name, self.time_delta)
