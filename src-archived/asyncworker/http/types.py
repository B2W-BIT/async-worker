from abc import abstractmethod
from typing import Generic, TypeVar, Type

import pydantic

from asyncworker.http.wrapper import RequestWrapper

T = TypeVar("T")


class BoolModel(pydantic.BaseModel):
    value: bool


class RequestParser(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value: T = value

    @classmethod
    @abstractmethod
    async def from_request(
        cls, request: RequestWrapper, arg_name: str, arg_type: Type
    ) -> "RequestParser[T]":
        raise NotImplementedError()

    async def unpack(self) -> T:
        return self._value


class PathParam(RequestParser[T]):
    @classmethod
    async def from_request(
        cls, request: RequestWrapper, arg_name: str, arg_type: Type
    ) -> "PathParam[T]":
        val = request.http_request.match_info[arg_name]
        if arg_type is bool:
            try:
                return cls(arg_type(BoolModel(value=val).value))
            except pydantic.ValidationError:
                return cls(arg_type(False))
        return cls(arg_type(val))
