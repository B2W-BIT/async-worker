from typing import List

from asynctest import TestCase

from asyncworker.types.registry import TypesRegistry
from asyncworker.types.resolver import ArgResolver


class ArgResolverTest(TestCase):
    async def test_wraps_coroutine_reference(self):
        async def my_coro():
            return 42

        resolver = ArgResolver(TypesRegistry())
        result = await resolver.wrap(my_coro)
        self.assertEqual(42, result)

    async def test_await_for_coro_one_param(self):
        class MyObject:
            pass

        async def my_coro(obj: MyObject):
            return obj

        instance = MyObject()
        registry = TypesRegistry()
        registry.set(instance)

        resolver = ArgResolver(registry)
        result = await resolver.wrap(my_coro)
        self.assertEqual(instance, result)

    async def test_await_for_coro_two_params(self):
        class MyObject:
            pass

        async def my_coro(obj: MyObject, num: int):
            return obj, num

        instance = MyObject()
        registry = TypesRegistry()
        registry.set(instance)
        registry.set(42)

        resolver = ArgResolver(registry)
        result = await resolver.wrap(my_coro)
        self.assertEqual((instance, 42), result)

    async def test_raises_ArgumentError_when_unresolved_args_exist(self):
        async def my_coro(num: int, value: str):
            return 1 / 0

        registry = TypesRegistry()
        registry.set(42)

        resolver = ArgResolver(registry)
        with self.assertRaises(TypeError):
            await resolver.wrap(my_coro)

    async def test_multiple_resolvers(self):
        async def coro(p: int, arg: str, other: bool):
            return (p, arg, other)

        registry_one = TypesRegistry()
        registry_one.set(42)

        registry_two = TypesRegistry()
        registry_two.set("string")
        registry_two.set(True)

        resolver = ArgResolver(registry_one, registry_two)
        result = await resolver.wrap(coro)
        self.assertEqual((42, "string", True), result)

    async def test_resolve_list_argument(self):
        async def my_coro(arg0: List[int], value: str):
            return arg0, value

        registry = TypesRegistry()
        registry.set([42, 42])
        registry.set("value")

        resolver = ArgResolver(registry)
        self.assertEqual(([42, 42], "value"), await resolver.wrap(my_coro))
