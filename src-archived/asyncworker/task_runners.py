import asyncio
import sys
from typing import Callable, Coroutine, Set, TYPE_CHECKING

from asyncworker.time import ClockTicker

if TYPE_CHECKING:
    from asyncworker.app import App  # pragma: nocover

BEFORE_PY_37 = sys.version_info[0:2] < (3, 7)

if BEFORE_PY_37:
    _current_task_func = asyncio.Task.current_task
else:
    _current_task_func = asyncio.current_task  # type: ignore


class ScheduledTaskRunner:
    def __init__(
        self,
        seconds: int,
        task: Callable[["App"], Coroutine],
        app: "App",
        max_concurrency: int,
    ) -> None:
        self.seconds = seconds
        self.max_concurrency = max_concurrency
        self.task = task
        self.app = app
        self.running_tasks: Set[asyncio.Future] = set()
        self.task_is_done_event = asyncio.Event()
        self._started = False
        self.clock = ClockTicker(seconds=self.seconds)

    async def can_dispatch_task(self) -> bool:
        if len(self.running_tasks) < self.max_concurrency:
            return True

        if await self.task_is_done_event.wait():
            return True
        return False

    async def _wrapped_task(self) -> None:
        """
        Wraps the future task on a coroutine that's responsible for unregistering
        itself from the "running tasks" and emitting an "task is done" event
        """
        try:
            await self.task(self.app)
        finally:
            self.task_is_done_event.set()
            self.running_tasks.remove(_current_task_func())

    async def start(self, app: "App") -> asyncio.Future:
        self._started = True
        return asyncio.ensure_future(self._run())

    async def stop(self, app: "App") -> None:
        await self.clock.stop()
        await asyncio.gather(*self.running_tasks)

    async def _run(self) -> None:
        async for tick in self.clock:
            if await self.can_dispatch_task():
                task = asyncio.ensure_future(self._wrapped_task())
                self.running_tasks.add(task)
                self.task_is_done_event.clear()
