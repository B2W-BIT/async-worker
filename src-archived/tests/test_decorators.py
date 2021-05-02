from asynctest import TestCase

from asyncworker.decorators import wraps
from asyncworker.types.registry import TypesRegistry
from asyncworker.types.resolver import ArgResolver
from asyncworker.typing import get_handler_original_typehints


def handler_register(func):
    async def _register_wrap(x: int = 0):
        return func

    return _register_wrap


def _deco(handler):
    @wraps(handler)
    async def _wrapper(s: str):
        pass

    return _wrapper


def _deco2(handler):
    @wraps(handler)
    async def _wrapper(param: bool, i: int):
        pass

    return _wrapper


def _deco3(handler):
    @wraps(handler)
    async def _wrapper(other: str, flag: bool):
        pass

    return _wrapper


class TestWrapsDecorator(TestCase):
    async def setUp(self):
        self.registry = TypesRegistry()
        self.resolver = ArgResolver(registry=self.registry)

    async def test_with_one_first_decorator(self):
        @handler_register
        @_deco
        async def _func(q: int, b: bool):
            pass

        final_func = await _func()
        self.assertEqual(final_func.__annotations__, {"s": str})
        self.assertEqual(
            get_handler_original_typehints(final_func), {"q": int, "b": bool}
        )
        self.assertEqual(
            "TestWrapsDecorator.test_with_one_first_decorator.<locals>._func",
            final_func.asyncworker_original_qualname,
        )

    async def test_with_two_second_decorators(self):
        @handler_register
        @_deco2
        @_deco
        async def _func(other: int, integer: int, feature: bool):
            pass

        final_func = await _func()
        self.assertEqual(final_func.__annotations__, {"param": bool, "i": int})
        self.assertEqual(
            get_handler_original_typehints(final_func),
            {"other": int, "integer": int, "feature": bool},
        )

        self.assertEqual(
            "TestWrapsDecorator.test_with_two_second_decorators.<locals>._func",
            final_func.asyncworker_original_qualname,
        )

    async def test_with_three_decorators(self):
        @handler_register
        @_deco3
        @_deco2
        @_deco
        async def _func(other: int, integer: int, feature: bool):
            pass

        final_func = await _func()
        self.assertEqual(
            final_func.__annotations__, {"flag": bool, "other": str}
        )
        self.assertEqual(
            get_handler_original_typehints(final_func),
            {"other": int, "integer": int, "feature": bool},
        )

    async def test_when_decorator_has_parameters(self):
        def _deco_with_params(a: int):
            def _wrap1(handler):
                @wraps(handler)
                async def _final_wrap(param: bool):
                    pass

                return _final_wrap

            return _wrap1

        @handler_register
        @_deco_with_params(42)
        async def _func(x: bool, y: int):
            pass

        final_func = await _func()
        self.assertEqual(final_func.__annotations__, {"param": bool})
        self.assertEqual(
            get_handler_original_typehints(final_func), {"x": bool, "y": int}
        )

    async def test_call_chain_one_decorator(self):
        registry = TypesRegistry()
        resolver = ArgResolver(registry=registry)

        def deco_final(_handler):
            @wraps(_handler)
            async def _wrap(p: str):
                registry.set(False)
                return await resolver.wrap(_handler)

            return _wrap

        def _handler_deco(handler):
            @wraps(handler)
            async def _handler_deco_wrap(x: bool):
                registry.set(42)
                registry.set(True)
                return await resolver.wrap(handler)

            return _handler_deco_wrap

        @deco_final
        @_handler_deco
        async def handler(p: int, flag: bool):
            return (p, flag)

        registry.set("is p")
        result = await resolver.wrap(handler)
        self.assertEqual((42, True), result)

    async def test_call_chain_two_decorators(self):
        """
        Cada decorator fornece (acumula) um dos parametros necessários 
        para o handler ser chamado
        """

        registry = self.registry
        resolver = self.resolver

        def deco_final(handler):
            """
            Inicia o call chain
            """

            @wraps(handler)
            async def wrap():
                return await resolver.wrap(handler)

            return wrap

        def deco1(handler):
            """
            Fornece o bool
            """

            @wraps(handler)
            async def wrap():
                registry.set(True)
                return await resolver.wrap(handler)

            return wrap

        def deco2(handler):
            """
            Fornecce a str
            """

            @wraps(handler)
            async def wrap():
                registry.set("String")
                return await resolver.wrap(handler)

            return wrap

        @deco_final
        @deco1
        @deco2
        async def handler(b: bool, c: str):
            return (b, c)

        result = await self.resolver.wrap(handler)
        self.assertEqual((True, "String"), result)
