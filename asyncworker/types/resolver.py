from asyncio import Task
from functools import wraps
from typing import List, Type, Coroutine, Dict, Any, Union

from asyncworker.types.registry import TypesRegistry


class ArgResolver:
    def __init__(
        self, registry: TypesRegistry, *extra_registries: List[TypesRegistry]
    ) -> None:
        self.registries: List[TypesRegistry] = [registry]
        self.registries.extend(extra_registries)

    def wrap(self, coro_ref):
        return Task(self._coro_executor(coro_ref))

    def resolve_param(self, param_type: Type) -> Union[Any, None]:
        for registry in self.registries:
            arg_value = registry.get(param_type)
            if arg_value:
                return arg_value

        return None

    async def _coro_executor(self, coro_ref: Type[Coroutine]):
        params: Dict[str, Any] = {}
        unresolved_params = []
        for param_name, param_type in coro_ref.__annotations__.items():
            param_value = self.resolve_param(param_type)
            if param_value:
                params[param_name] = param_value
            else:
                unresolved_params.append((param_name, param_type))
        if unresolved_params:
            raise TypeError(
                f"Unresolved params for coroutine {coro_ref}: {unresolved_params}"
            )
        return await coro_ref(**params)
