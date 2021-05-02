from typing import Generic, TypeVar

from asynctest import TestCase

from asyncworker.decorators import wraps
from asyncworker.typing import (
    get_handler_original_qualname,
    is_base_type,
    get_args,
    get_origin,
    get_handler_original_typehints,
)

T = TypeVar("T")
K = TypeVar("K")


class MyGeneric(Generic[T]):
    pass


class MyGenericTwoArguments(Generic[K, T]):
    pass


class MyObject:
    pass


class TestTypingFunctions(TestCase):
    async def setUp(self):
        pass

    async def test_get_args_generic_type(self):
        self.assertEqual((MyObject,), get_args(MyGeneric[MyObject]))
        self.assertEqual(
            (int, MyObject), get_args(MyGenericTwoArguments[int, MyObject])
        )

    async def test_get_args_concrete_type(self):
        self.assertIsNone(get_args(MyObject))

    async def test_get_origin_generic_type(self):
        self.assertEqual(MyGeneric, get_origin(MyGeneric[MyObject]))
        self.assertEqual(
            MyGenericTwoArguments,
            get_origin(MyGenericTwoArguments[int, MyObject]),
        )

    async def test_get_origin_concrete_type(self):
        self.assertIsNone(get_origin(MyObject))


class TestGetOriginalHandlerTypeHints(TestCase):
    async def test_does_not_have_attribute(self):
        def func(a: int, b: bool):
            pass

        self.assertEqual(
            get_handler_original_typehints(func), {"a": int, "b": bool}
        )
        self.assertFalse(hasattr(func, "asyncworker_original_annotations"))

    async def test_has_attribute(self):
        def simple_deco(handler):
            @wraps(handler)
            async def _wrapper():
                return await handler()

            return _wrapper

        def other_deco(handler):
            @wraps(handler)
            async def _wrap():
                return get_handler_original_typehints(handler)

            return _wrap

        @other_deco
        @simple_deco
        async def handler(a: bool, s: str):
            return 42

        result = await handler()
        self.assertEqual(result, {"a": bool, "s": str})
        self.assertTrue(hasattr(handler, "asyncworker_original_annotations"))


class TestIsBaseType(TestCase):
    async def test_is_base_when_generic(self):
        def _func(b: MyGeneric[int]):
            pass

        _type = get_handler_original_typehints(_func)
        self.assertTrue(is_base_type(_type["b"], MyGeneric))

    async def test_is_base_when_not_generic(self):
        def _func(b: MyGeneric):
            pass

        _type = get_handler_original_typehints(_func)
        self.assertTrue(is_base_type(_type["b"], MyGeneric))

    async def test_is_base_when_arg_generic_base_primitive(self):
        def _func(b: MyGeneric):
            pass

        _type = get_handler_original_typehints(_func)
        self.assertFalse(is_base_type(_type["b"], int))

    async def test_is_base_when_arg_primitive_base_generic(self):
        def _func(b: int):
            pass

        _type = get_handler_original_typehints(_func)
        self.assertFalse(is_base_type(_type["b"], MyGeneric))


class TestHandlerGetOriginalQualname(TestCase):
    async def test_get_qualname_no_decorators(self):
        async def handler(a: bool, s: str):
            return 42

        self.assertEqual(
            "TestHandlerGetOriginalQualname.test_get_qualname_no_decorators.<locals>.handler",
            get_handler_original_qualname(handler),
        )
        self.assertFalse(hasattr(handler, "asyncworker_original_qualname"))

    async def test_get_qualname_with_decorators(self):
        def other_deco(handler):
            @wraps(handler)
            async def _wrap():
                return get_handler_original_typehints(handler)

            return _wrap

        @other_deco
        async def handler(a: bool, s: str):
            return 42

        self.assertEqual(
            "TestHandlerGetOriginalQualname.test_get_qualname_with_decorators.<locals>.handler",
            get_handler_original_qualname(handler),
        )
        self.assertTrue(hasattr(handler, "asyncworker_original_qualname"))
