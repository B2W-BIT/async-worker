def wraps(original_handler):
    """
    Esse decorator faz com que a assinatura da função original
    "suba" até o último decorator, que deverá ser sempre um registrador do
    próprio asyncworker. ex:
    @app.http.get(...)
    @deco1
    @deco2
    async def handler(...)
        pass

    Nesse caso, os decorators `@deco1` e `@deco2` devem, *necessariamente*
    fazer uso desse `@wraps()`
    """

    def _wrap(deco):
        deco.asyncworker_original_annotations = getattr(
            original_handler,
            "asyncworker_original_annotations",
            original_handler.__annotations__,
        )
        deco.asyncworker_original_qualname = getattr(
            original_handler,
            "asyncworker_original_qualname",
            original_handler.__qualname__,
        )
        return deco

    return _wrap
