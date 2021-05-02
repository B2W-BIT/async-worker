import inspect
import typing
from asyncio import Task
from typing import List, Type, Coroutine, Dict, Any, Union, Callable

from asyncworker.types.registry import TypesRegistry


class MissingTypeAnnotationError(Exception):
    pass


class ArgResolver:
    def __init__(
        self, registry: TypesRegistry, *extra_registries: TypesRegistry
    ) -> None:
        self.registries: List[TypesRegistry] = [registry]
        self.registries.extend(extra_registries)

    def wrap(self, coro_ref):
        return Task(self._coro_executor(coro_ref))

    def resolve_param(
        self, param_type: Type, param_name: str
    ) -> Union[Any, None]:
        for registry in self.registries:
            arg_value = registry.get(param_type, param_name=param_name)
            if arg_value is not None:
                return arg_value

            arg_value = registry.get(param_type)
            if arg_value is not None:
                return arg_value

        return None

    async def _coro_executor(self, coro_ref: Callable[..., Coroutine]):
        params: Dict[str, Any] = {}
        unresolved_params = []
        coro_arguments = inspect.signature(coro_ref).parameters
        type_annotations = typing.get_type_hints(coro_ref)
        type_annotations.pop("return", None)

        if coro_arguments:
            if not type_annotations:
                raise MissingTypeAnnotationError(
                    f"{coro_ref} has no type annotation"
                )

            for param_name, param_type in type_annotations.items():
                param_value = self.resolve_param(param_type, param_name)
                if param_value is not None:
                    params[param_name] = param_value
                else:
                    unresolved_params.append((param_name, param_type))
            if unresolved_params:
                raise TypeError(
                    f"Unresolved params for coroutine {coro_ref}: {unresolved_params}"
                )
        return await coro_ref(**params)
