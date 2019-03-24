from typing import Type, Any, List


class TypesRegistry:
    def __init__(self):
        self.__data = {}

    def set(self, obj, type_definition=None):
        if isinstance(obj, list):
            cl = List[obj[0].__class__] if obj else type_definition
            self.__data[cl] = obj
        else:
            self.__data[obj.__class__] = obj

    def get(self, _type: Type) -> Any:
        return self.__data.get(_type, None)
