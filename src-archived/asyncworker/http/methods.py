from enum import auto

from asyncworker.options import AutoNameEnum


class HTTPMethods(AutoNameEnum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()
    HEAD = auto()
