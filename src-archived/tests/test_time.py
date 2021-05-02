import asyncio

import asynctest
from asynctest import CoroutineMock, patch, Mock

from asyncworker.time import ClockTicker


class ClockTickerTests(asynctest.TestCase):
    async def test_a_stoped_clock_cannot_be_reused(self):
        clock = ClockTicker(seconds=0.0001)

        async for tick in clock:
            await clock.stop()

        with self.assertRaises(RuntimeError):
            async for tick in clock:
                self.fail("Shouldnt be possible to iter on a stopped clock")

    async def test_anext_waits_for_a_tick(self):
        clock = ClockTicker(seconds=0.1)

        async def my_task():
            async for tick in clock:
                await asyncio.sleep(0.2)

        self.loop.create_task(my_task())
        await asyncio.sleep(0.3)
        await clock.stop()

        self.assertEqual(2, clock.current_iteration)

    async def test_stop_stops_the_current_clock_ticker(self):
        clock = ClockTicker(seconds=2)
        clock._running = True
        _main_task = CoroutineMock()
        with asynctest.patch.object(clock, "_main_task", _main_task()):
            await clock.stop()

            _main_task.assert_awaited_once()
            self.assertFalse(clock._running)

    async def test_run_should_set_the_tick_event_everytime_an_interval_is_passed(
        self
    ):
        event = Mock()
        with patch("asyncworker.time.asyncio.Event", return_value=event):

            async def tick_check(clock: ClockTicker):
                event.set.assert_called_once()
                event.clear.assert_not_called()
                await clock.stop()

            clock = ClockTicker(seconds=2)
            sleep = CoroutineMock(side_effect=lambda seconds: tick_check(clock))

            with patch("asyncworker.time.asyncio.sleep", sleep):
                clock._running = True
                task = self.loop.create_task(clock._run())
                await task
                event.clear.assert_called_once()
                sleep.assert_awaited_once_with(2)
