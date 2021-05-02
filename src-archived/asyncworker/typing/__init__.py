from typing import Optional, Tuple, Type, get_type_hints


def get_args(_type: Optional[Type]) -> Optional[Tuple]:
    if _type and hasattr(_type, "__args__"):
        return _type.__args__

    return None


def get_origin(_type: Optional[Type]) -> Optional[Type]:
    if _type and hasattr(_type, "__origin__"):
        return _type.__origin__

    return None


def get_handler_original_typehints(handler):
    """
    Retorna a assinatura do handler asyncworker que está sendo decorado.
    O retorno dessa chamada é equivalente a:
    typing.get_type_hints(original_handler)
    Onde `original_handler` é o handler asyncworker original.

    Ideal para ser usado na pilha de decorators de um handler, ex:

    .. code-block:: python

        @deco1
        @deco2
        @deco3
        async def handler(...):
            pass

    Nesse caso, se qualquer um dos 3 decorators precisar saber a assinatura
    original, deve usar essa função passando a função recebida do decorator anterior.

    """

    def _dummy():
        pass

    _dummy.__annotations__ = getattr(
        handler, "asyncworker_original_annotations", handler.__annotations__
    )

    return get_type_hints(_dummy)


def is_base_type(_type, base_type):
    """
    Retorna True para argumentos de um tipo base `base_type`.
    Ex:
    (a: MyGeneric[int]) -> True
    (b: MyGeneric) -> True
    """
    if get_origin(_type) is base_type:
        return True

    return issubclass(_type, base_type)


def get_handler_original_qualname(handler):
    return getattr(
        handler, "asyncworker_original_qualname", handler.__qualname__
    )
