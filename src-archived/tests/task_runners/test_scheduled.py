import asyncio
import sys
from importlib import reload

import asynctest
from asynctest import CoroutineMock, patch, call, Mock, skip

from asyncworker import task_runners
from asyncworker.app import App
from asyncworker.task_runners import ScheduledTaskRunner


class ScheduledTaskRunnerTests(asynctest.TestCase):
    async def setUp(self):
        reload(task_runners)
        self.task = CoroutineMock()
        self.app = asynctest.Mock(spec=App)
        self.seconds = 10
        self.max_concurrency = 2

        self.task_runner = ScheduledTaskRunner(
            seconds=self.seconds,
            task=self.task,
            app=self.app,
            max_concurrency=self.max_concurrency,
        )

    async def test_it_can_dispatch_a_new_task_if_running_tasks_doesnt_exceed_max_concurrency(
        self
    ):
        self.task_runner.running_tasks = {CoroutineMock()}

        self.assertTrue(await self.task_runner.can_dispatch_task())

    async def test_it_waits_for_a_task_to_be_completed_before_dispatching_a_new_task_if_running_tasks_reached_max_concurrency(
        self
    ):
        self.task_runner.running_tasks = {CoroutineMock(), CoroutineMock()}

        with patch.object(self.task_runner.task_is_done_event, "wait") as wait:
            self.assertTrue(await self.task_runner.can_dispatch_task())
            wait.assert_awaited_once()

    async def test_wrapped_task_awaits_for_the_task(self):
        wrapped_task = asyncio.ensure_future(self.task_runner._wrapped_task())

        self.task_runner.running_tasks.add(wrapped_task)
        await wrapped_task

        self.task.assert_awaited_once_with(self.app)

    async def test_wrapped_task_unregisters_itself_from_the_running_tasks(self):
        wrapped_task = asyncio.ensure_future(self.task_runner._wrapped_task())

        self.task_runner.running_tasks.add(wrapped_task)
        await wrapped_task
        self.assertEqual(len(self.task_runner.running_tasks), 0)

    async def test_wrapped_task_emits_the_task_is_done_event_if_task_finishes_successfully(
        self
    ):
        with patch.object(self.task_runner.task_is_done_event, "set") as set:
            wrapped_task = asyncio.ensure_future(
                self.task_runner._wrapped_task()
            )

            self.task_runner.running_tasks.add(wrapped_task)
            await wrapped_task
            set.assert_called_once()

    async def test_wrapped_task_emits_the_task_is_done_event_if_task_raises_an_error(
        self
    ):
        with patch.object(self.task_runner.task_is_done_event, "set") as set:
            self.task.side_effect = error = ConnectionError
            wrapped_task = asyncio.ensure_future(
                self.task_runner._wrapped_task()
            )

            self.task_runner.running_tasks.add(wrapped_task)
            with self.assertRaises(error):
                await wrapped_task

            set.assert_called_once()

    async def test_start_creates_a_background_task_for_run(self):
        self.assertFalse(self.task_runner._started)

        with patch.object(self.task_runner, "_run") as _run, patch(
            "asyncworker.task_runners.asyncio.ensure_future"
        ) as ensure_future:
            await self.task_runner.start(self.app)

            self.assertTrue(self.task_runner._started)
            _run.assert_called_once()
            ensure_future.assert_called_once()

    async def test_stop_stops_the_underlying_clock_ticker(self):
        with patch.object(self.task_runner.clock, "stop") as clock_stop:
            await self.task_runner.stop(self.app)
            clock_stop.assert_awaited_once()

    async def test_stop_awaits_for_the_currently_running_tasks_to_end(self):
        t1, t2 = CoroutineMock(), CoroutineMock()
        self.task_runner.running_tasks = {t1(), t2()}
        with patch.object(self.task_runner.clock, "stop"):
            await self.task_runner.stop(self.app)

            t1.assert_awaited_once()
            t2.assert_awaited_once()

    async def test_run_follows_the_clock_tick(self):
        clock = asynctest.MagicMock()
        clock.__aiter__.return_value = range(3)

        with patch.multiple(
            self.task_runner,
            clock=clock,
            can_dispatch_task=CoroutineMock(return_value=False),
        ):
            await self.task_runner._run()
            self.task_runner.can_dispatch_task.assert_has_awaits(
                [call(), call(), call()]
            )

    async def test_current_task_compatiple_with_py36_plus(self):
        async def _task(app: App):
            return None

        task_runner = ScheduledTaskRunner(
            seconds=self.seconds,
            task=_task,
            app=self.app,
            max_concurrency=self.max_concurrency,
        )

        def _current_task():
            return _task

        with patch.object(
            asyncio, "current_task", _current_task, create=True
        ), patch.object(sys, "version_info", (3, 8)):
            reload(task_runners)
            task_runner.running_tasks.add(_task)
            await task_runner._wrapped_task()
            self.assertTrue(_task not in task_runner.running_tasks)

    async def test_current_task_compatiple_with_py36(self):
        async def _task(app: App):
            return None

        task_runner = ScheduledTaskRunner(
            seconds=self.seconds,
            task=_task,
            app=self.app,
            max_concurrency=self.max_concurrency,
        )

        def _current_task():
            return _task

        with patch.object(
            asyncio, "Task", _current_task
        ) as Task_mock, patch.object(sys, "version_info", (3, 6)):
            Task_mock.current_task = _current_task
            reload(task_runners)
            task_runner.running_tasks.add(_task)
            await task_runner._wrapped_task()
            self.assertTrue(_task not in task_runner.running_tasks)

    async def test_run_dispatches_a_new_task_for_each_valid_clock_tick(self):
        clock = asynctest.MagicMock()
        clock.__aiter__.return_value = range(3)
        wrapped_task = Mock()
        with patch.multiple(
            self.task_runner,
            clock=clock,
            _wrapped_task=wrapped_task,
            can_dispatch_task=CoroutineMock(side_effect=[True, False, True]),
        ), patch(
            "asyncworker.task_runners.asyncio.ensure_future"
        ) as ensure_future:
            await self.task_runner._run()
            self.assertEqual(
                ensure_future.call_args_list,
                [
                    call(wrapped_task.return_value),
                    call(wrapped_task.return_value),
                ],
            )

    async def test_run_emits_a_task_i_done_event_for_each_valid_clock_tick(
        self
    ):
        clock = asynctest.MagicMock()
        clock.__aiter__.return_value = range(3)
        wrapped_task = Mock()
        with patch.multiple(
            self.task_runner,
            clock=clock,
            _wrapped_task=wrapped_task,
            task_is_done_event=Mock(),
            can_dispatch_task=CoroutineMock(side_effect=[True, False, True]),
        ), patch("asyncworker.task_runners.asyncio.ensure_future"):
            await self.task_runner._run()

            self.task_runner.task_is_done_event.clear.assert_has_calls(
                [call(), call()]
            )

    async def test_run_adds_the_new_task_for_each_valid_clock_tick(self):
        clock = asynctest.MagicMock()
        clock.__aiter__.return_value = range(3)
        wrapped_task = Mock()
        with patch.multiple(
            self.task_runner,
            clock=clock,
            _wrapped_task=wrapped_task,
            running_tasks=Mock(spec=set),
            can_dispatch_task=CoroutineMock(side_effect=[True, False, True]),
        ), patch(
            "asyncworker.task_runners.asyncio.ensure_future"
        ) as ensure_future:
            await self.task_runner._run()

            self.task_runner.running_tasks.add.assert_has_calls(
                [
                    call(ensure_future.return_value),
                    call(ensure_future.return_value),
                ]
            )
