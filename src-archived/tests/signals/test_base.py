import asynctest
from asynctest import Mock, CoroutineMock

from asyncworker.signals.base import Signal


class SignalTests(asynctest.TestCase):
    async def setUp(self):
        self.owner = Mock(freeze=CoroutineMock())
        self.signal = Signal(self.owner)

    async def test_send_raises_an_error_if_signal_is_frozen(self):
        self.signal.frozen = True
        with self.assertRaises(RuntimeError):
            await self.signal.send()

    async def test_send_sends_data_to_all_registered_receivers(self):
        handlers = [CoroutineMock(), CoroutineMock(), CoroutineMock()]
        self.signal.extend(handlers)
        args = [1, 2, 3]
        kwargs = {"dog": "Xablau"}

        await self.signal.send(*args, **kwargs)

        self.owner.freeze.assert_awaited_once()
        for handler in handlers:
            handler.assert_awaited_once_with(*args, **kwargs)
