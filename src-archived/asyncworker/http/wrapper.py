from aiohttp.web import Request

from asyncworker.types.registry import TypesRegistry


class RequestWrapper:
    http_request: Request
    types_registry: TypesRegistry

    def __init__(
        self, http_request: Request, types_registry: TypesRegistry
    ) -> None:
        self.http_request = http_request
        self.types_registry = types_registry
