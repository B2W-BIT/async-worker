from typing import Tuple

from asynctest import TestCase

from asyncworker.types.registry import TypesRegistry
from asyncworker.types.resolver import ArgResolver, MissingTypeAnnotationError


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

    async def test_reolves_args_that_is_falsy(self):
        """
        Mesmo o objeto sendo bool(arg) == False temos que conseguir
        resolvê-lo
        """

        class MyObject:
            def __bool__(self):
                return False

        async def my_coro(obj: MyObject):
            return obj

        instance = MyObject()
        registry = TypesRegistry()
        registry.set(instance)

        resolver = ArgResolver(registry)
        result = await resolver.wrap(my_coro)
        self.assertEqual(instance, result)

    async def test_resolve_multiple_coros_with_same_registry(self):
        async def coro(p: int):
            return p

        registry_one = TypesRegistry()
        registry_one.set(42)

        resolver = ArgResolver(registry_one)
        result = await resolver.wrap(coro)
        self.assertEqual(42, await resolver.wrap(coro))

        resolver2 = ArgResolver(registry_one)
        self.assertEqual(42, await resolver2.wrap(coro))

        self.assertEqual(42, registry_one.get(int))

    async def test_resolves_coro_with_return_annotation(self):
        async def my_coro(arg0: int, value: str) -> Tuple[int, str]:
            return arg0, value

        registry = TypesRegistry()
        registry.set(42)
        registry.set("value")

        resolver = ArgResolver(registry)
        self.assertEqual((42, "value"), await resolver.wrap(my_coro))

    async def test_raise_argument_error_if_coro_has_no_type_annotation(self):
        async def my_coro(arg0):
            return arg0

        registry = TypesRegistry()
        registry.set([42, 42])
        registry.set("value")

        resolver = ArgResolver(registry)
        with self.assertRaises(MissingTypeAnnotationError):
            await resolver.wrap(my_coro)

    async def test_calls_corotine_with_no_arguments(self):
        async def my_coro():
            return 42

        registry = TypesRegistry()
        registry.set([42, 42])
        registry.set("value")

        resolver = ArgResolver(registry)
        self.assertEqual(42, await resolver.wrap(my_coro))

    async def test_prefer_named_paramteres_before_typed_parameters(self):
        """
        Primeiro sempre tentamos pegar o paramtero pelo nome, só depois
        pegamos o valor olhando apenas o tipo
        """

        async def my_coro(arg0: int, value: int):
            return arg0, value

        registry = TypesRegistry()
        registry.set(42, param_name="arg0")
        registry.set(44, param_name="value")

        resolver = ArgResolver(registry)
        self.assertEqual((42, 44), await resolver.wrap(my_coro))
