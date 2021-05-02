import unittest
from unittest.mock import patch, Mock

import asynctest as asynctest
from freezegun import freeze_time

from asyncworker.utils import Timeit
from tests.utils import typed_any


class TimeitTests(asynctest.TestCase):
    time = 1_149_573_966.0

    @freeze_time("2006-06-06 06:06:06")
    async def test_it_marks_starting_times(self):
        coro = asynctest.CoroutineMock()
        async with Timeit(name="Xablau", callback=coro) as timeit:
            self.assertEqual(timeit.start, 1_149_573_966.0)

    @freeze_time("2006-06-06 06:06:07")
    async def test_it_marks_finishing_times(self):
        coro = asynctest.CoroutineMock()
        async with Timeit(name="Xablau", callback=coro) as timeit:
            pass
        self.assertEqual(timeit.finish, 1_149_573_967.0)

    async def test_it_calculates_time_delta(self):
        now = Mock(side_effect=[self.time, self.time + 1])
        with patch("asyncworker.utils.now", now):
            async with Timeit(
                name="Xablau", callback=asynctest.CoroutineMock()
            ) as timeit:
                pass

        self.assertEqual(timeit._transactions["Xablau"], 1.0)

    async def test_it_calls_callback_on_context_end(self):
        callback = asynctest.CoroutineMock()
        times = [self.time, self.time + 1]
        with patch("asyncworker.utils.now", Mock(side_effect=times)):
            async with Timeit(name="Xablau", callback=callback) as timeit:
                callback.assert_not_awaited()
        callback.assert_awaited_once_with(
            **{
                Timeit.TRANSACTIONS_KEY: timeit._transactions,
                "exc_type": None,
                "exc_val": None,
                "exc_tb": None,
            }
        )

    async def test_it_calls_callback_with_exc_parameters_if_an_exception_is_raised(
        self
    ):
        coro = asynctest.CoroutineMock()
        try:
            async with Timeit(name="Xablau", callback=coro) as timeit:
                raise KeyError("Xablau")
        except KeyError as e:
            coro.assert_awaited_once_with(
                **{
                    Timeit.TRANSACTIONS_KEY: timeit._transactions,
                    "exc_type": KeyError,
                    "exc_val": e,
                    "exc_tb": e.__traceback__,
                }
            )

    async def test_it_can_be_used_as_a_decorator(self):
        coro = asynctest.CoroutineMock()
        now = Mock(side_effect=[self.time, self.time + 1])

        @Timeit(name="Xablau", callback=coro)
        async def foo():
            pass

        with patch("asyncworker.utils.now", now):
            await foo()

        coro.assert_awaited_once_with(
            **{
                Timeit.TRANSACTIONS_KEY: {"Xablau": 1.0},
                "exc_type": None,
                "exc_val": None,
                "exc_tb": None,
            }
        )

    async def test_timeit_children_share_a_common_transactions_state(self):
        callback = asynctest.CoroutineMock()
        async with Timeit(name="a", callback=callback) as timeit:
            pass
            async with timeit(name="b") as child1:
                self.assertEqual(
                    id(child1._transactions), id(timeit._transactions)
                )
                async with timeit(name="c") as child2:
                    self.assertEqual(
                        id(child2._transactions), id(timeit._transactions)
                    )

    async def test_initializing_more_than_one_transation_with_the_same_name_on_the_same_scope_raises_an_error(
        self
    ):
        callback = asynctest.CoroutineMock()
        with self.assertRaises(ValueError):
            async with Timeit(name="a", callback=callback) as timeit:
                pass
                async with timeit(name="a"):
                    pass

    async def test_it_can_have_multiple_nested_transactions(self):
        callback = asynctest.CoroutineMock()
        now = Mock(
            side_effect=[
                self.time,
                self.time,
                self.time,
                self.time + 1,
                self.time + 2,
                self.time + 3,
            ]
        )

        with patch("asyncworker.utils.now", now):

            async with Timeit(name="a", callback=callback) as timeit:
                # do some database access
                async with timeit(name="b"):
                    # do some processing
                    async with timeit(name="c"):
                        """do some other time costly stuff"""

        callback.assert_awaited_once_with(
            **{
                Timeit.TRANSACTIONS_KEY: {"a": 3.0, "b": 2.0, "c": 1.0},
                "exc_type": None,
                "exc_val": None,
                "exc_tb": None,
            }
        )


class TypedAnyTests(unittest.TestCase):
    def test_instances_of_the_same_classes_are_equal(self):
        self.assertEqual(5, typed_any(int))
        self.assertEqual("abc", typed_any(str))
        self.assertEqual(Exception(), typed_any(ValueError))

    def test_isntances_of_different_calsses_arent_equal(self):
        self.assertNotEqual(5, typed_any(str))
        self.assertNotEqual("abc", typed_any(int))
        self.assertNotEqual(ValueError(), typed_any(Exception))
