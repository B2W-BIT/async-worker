import typing

from aiohttp import web

from asyncworker.conf import logger
from asyncworker.routes import call_http_handler


def parse_path(handler):
    handler_types_args = typing.get_type_hints(handler)
    handler_args_names = list(handler_types_args.keys())

    async def _wrap(req: web.Request):

        for param_name in handler_args_names:
            if param_name in req.match_info:
                try:
                    value = handler_types_args[param_name](
                        req.match_info[param_name]
                    )
                    req["types_registry"].set(value, param_name=param_name)
                except ValueError:
                    await logger.exception(
                        {
                            "event": "incompatible-types-handler-arg",
                            "arg-type": handler_types_args[param_name],
                            "arg-value": req.match_info[param_name],
                        }
                    )
                    raise

        return await call_http_handler(req, handler)

    return _wrap
