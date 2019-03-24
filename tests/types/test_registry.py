from typing import List

from asynctest import TestCase

from asyncworker.types.registry import TypesRegistry


class TypesRegistryTest(TestCase):
    async def setUp(self):
        self.registry = TypesRegistry()

    async def test_simple_set_get_object(self):
        class SomeObject:
            pass

        instance = SomeObject()
        self.registry.set(instance)
        self.assertEqual(instance, self.registry.get(SomeObject))

    async def test_get_object_not_found(self):
        class OtherObject:
            pass

        self.assertIsNone(self.registry.get(OtherObject))

    async def test_get_object_of_list_type(self):
        """
        Searching for List[Class]
        """

        class MyClass:
            pass

        _list = [MyClass(), MyClass()]
        self.registry.set(_list)
        self.assertEqual(_list, self.registry.get(List[MyClass]))

    async def test_get_object_list_type_empty_list(self):
        class MyClass:
            pass

        _list: List[MyClass] = []
        self.registry.set(_list, List[MyClass])
        self.assertEqual(_list, self.registry.get(List[MyClass]))

    async def test_simple_coroutine_with_typehint(self):
        class MyClass:
            pass

        async def my_coro(p: MyClass):
            return p

        instance = MyClass()
        self.assertTrue(instance)
