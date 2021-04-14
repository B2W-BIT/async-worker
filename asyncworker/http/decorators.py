import typing

from asyncworker.conf import logger
from asyncworker.decorators import wraps
from asyncworker.http.wrapper import RequestWrapper
from asyncworker.routes import call_http_handler


def parse_path(handler):
    """
    Aqui usamos essa função `_dummy` apenas para aproveitar a implementação
    já existente em `typing.get_type_hints()`. 
    Como essa implementação exige que passamos uma function, mas temos nesse momento
    apenas um dict.
    Então criamos essa função "vazia" e colocmos nela as anotações do handler
    original.
    """

    def _dummy():
        pass

    _dummy.__annotations__ = getattr(
        handler, "asyncworker_original_annotations", handler.__annotations__
    )

    handler_types_args = typing.get_type_hints(_dummy)
    handler_args_names = list(handler_types_args.keys())

    @wraps(handler)
    async def _wrap(wrapper: RequestWrapper):
        req = wrapper.http_request

        for param_name in handler_args_names:
            if param_name in req.match_info:
                try:
                    value = handler_types_args[param_name](
                        req.match_info[param_name]
                    )
                    wrapper.types_registry.set(value, param_name=param_name)
                except ValueError:
                    await logger.exception(
                        {
                            "event": "incompatible-types-handler-arg",
                            "arg-type": handler_types_args[param_name],
                            "arg-value": req.match_info[param_name],
                        }
                    )
                    raise

        return await call_http_handler(wrapper, handler)

    return _wrap
