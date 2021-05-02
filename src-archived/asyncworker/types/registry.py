from typing import Type, Any, Dict, Optional, Tuple

from asyncworker.typing import get_args, get_origin


class RegistryItem:
    def __init__(self, type: Type, value: Any, type_args: Tuple = None) -> None:
        self.type = type
        self.value = value
        self.type_args = type_args


class TypesRegistry:
    def __init__(self):
        self._data: Dict[Tuple, RegistryItem] = {}
        self._by_name: Dict[str, RegistryItem] = {}

    def set(
        self,
        obj: Any,
        type_definition: Type = None,
        param_name: Optional[str] = None,
    ) -> None:
        has_type_args = get_args(type_definition)
        origin = get_origin(obj) or obj.__class__

        registry_item = RegistryItem(
            type=origin, value=obj, type_args=has_type_args
        )

        self._data[(origin, has_type_args)] = registry_item

        if param_name:
            self._by_name[param_name] = registry_item

    def get(
        self, _type: Type, param_name: str = None, type_args=None
    ) -> Optional[Any]:
        origin = get_origin(_type) or _type
        _type_args = type_args or get_args(_type)
        if param_name:
            try:
                item = self._by_name[param_name]
                if (item.type, item.type_args) == (origin, _type_args):
                    return item.value
            except KeyError:
                return None

        try:
            return self._data[(origin, get_args(_type))].value
        except KeyError:
            return None
