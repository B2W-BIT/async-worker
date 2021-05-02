from abc import ABC
from asyncio import iscoroutinefunction
from typing import Generic, TypeVar

import asyncworker
from asyncworker.routes import RouteHandler

T = TypeVar("T")


def _extract_async_callable(handler) -> RouteHandler:

    cb = handler

    if not iscoroutinefunction(cb):
        try:
            cb = handler.__call__
            if not iscoroutinefunction(cb):
                raise TypeError(f"handler must be async: {cb}")
        except AttributeError as e:
            raise TypeError(f"Object passed as handler is not callable: {cb}")

    return cb


class EntrypointInterface(ABC, Generic[T]):
    def __init__(self, app: "asyncworker.App") -> None:
        self.app = app
