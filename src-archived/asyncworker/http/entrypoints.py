from typing import Callable, List, Type

from aiohttp.web import HTTPBadRequest

from asyncworker.decorators import wraps
from asyncworker.entrypoints import _extract_async_callable, EntrypointInterface
from asyncworker.http import HTTPMethods
from asyncworker.http.types import PathParam
from asyncworker.http.wrapper import RequestWrapper
from asyncworker.routes import RoutesRegistry, HTTPRoute, call_http_handler
from asyncworker.typing import (
    is_base_type,
    get_args,
    get_handler_original_typehints,
    get_handler_original_qualname,
)


class RequestParserAnnotationSpec:
    def __init__(self, name: str, base: Type, arg_type: Type) -> None:
        self.name = name
        self.base = base
        self.arg_type = arg_type


def _install_request_parser_annotation(f, base_generic_type: Type):
    handler_type_hints = get_handler_original_typehints(f)
    path_params: List[RequestParserAnnotationSpec] = []

    for name, _type in handler_type_hints.items():
        if is_base_type(_type, base_generic_type):
            generic_type_args = get_args(_type)
            if not generic_type_args:
                raise TypeError(
                    f"{base_generic_type} must be Generic Type. Your handler {get_handler_original_qualname(f)} declares a parametrer that's not {base_generic_type}[T]"
                )
            if generic_type_args:
                path_params.append(
                    RequestParserAnnotationSpec(
                        name=name, base=_type, arg_type=generic_type_args[0]
                    )
                )

    @wraps(f)
    async def _wrap(wrapper: RequestWrapper):
        for p in path_params:
            try:
                typed_val = await p.base.from_request(
                    request=wrapper, arg_name=p.name, arg_type=p.arg_type
                )
                wrapper.types_registry.set(typed_val, p.base, param_name=p.name)
            except ValueError as e:
                raise HTTPBadRequest(text=e.args[0])
        return await call_http_handler(wrapper, f)

    return _wrap


def _register_http_handler(
    registry: RoutesRegistry, routes: List[str], method: HTTPMethods
) -> Callable:
    def _wrap(f):

        cb = _extract_async_callable(f)

        cb_with_parse_path = _install_request_parser_annotation(cb, PathParam)
        route = HTTPRoute(
            handler=cb_with_parse_path, routes=routes, methods=[method]
        )
        registry.add_http_route(route)

        return f

    return _wrap


class HTTPEntryPointImpl(EntrypointInterface):
    def _route(self, routes: List[str], method: HTTPMethods) -> Callable:
        return _register_http_handler(self.app.routes_registry, routes, method)

    def get(self, routes: List[str]) -> Callable:
        return self._route(routes=routes, method=HTTPMethods.GET)

    def head(self, routes: List[str]) -> Callable:
        return self._route(routes=routes, method=HTTPMethods.HEAD)

    def delete(self, routes: List[str]) -> Callable:
        return self._route(routes=routes, method=HTTPMethods.DELETE)

    def patch(self, routes: List[str]) -> Callable:
        return self._route(routes=routes, method=HTTPMethods.PATCH)

    def post(self, routes: List[str]) -> Callable:
        return self._route(routes=routes, method=HTTPMethods.POST)

    def put(self, routes: List[str]) -> Callable:
        return self._route(routes=routes, method=HTTPMethods.PUT)
