import unittest

from asyncworker.utils import entrypoint


class EntryPointTest(unittest.TestCase):
    def test_can_call_function_passing_positional_arguments(self):
        @entrypoint
        async def main(p1, p2, p3):
            return (p1, p2, p3)

        self.assertEqual((1, 2, 3), main(1, 2, 3))

    def test_can_call_function_passing_keywork_arguments(self):
        @entrypoint
        async def main(p1=None, p2=30):
            return (p1, p2)

        self.assertEqual((10, 44), main(p1=10, p2=44))

    def test_can_call_function_with_arbitrary_parameters(self):
        @entrypoint
        async def main(p1, p2, p3=10, p4=20):
            return (p1, p2, p3, p4)

        self.assertEqual((30, "str", 20, 42), main(30, "str", 20, p4=42))

    def test_call_run_until_complete(self):
        """
        Confirma que conseguimos pegar o return value da
        função que está sendo chamada
        """

        async def func(num):
            return num

        @entrypoint
        async def main():
            return await func(42)

        self.assertEqual(42, main())
