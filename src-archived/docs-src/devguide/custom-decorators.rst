.. _custom-decorators:

Aplicando decorators customizados a um handler HTTP
=====================================================

É possível escrever seus próprios decorators e aplicá-los a seus handlers, junto com os decorators ``@app.http.*``. No entando temos algumas regras:

- O decorator ``@app.http.*()`` deve estar sempre no topo da lista de decorators de um handler;
- Os decorators intermediários devem sempre usar a função :py:func:`asyncworker.routes.call_http_handler()` no momento de chamar o objeto que estão decorando;
- A inner function retornada pelo decorator deve ser uma corotina;
- A inner function deve receber apenas :py:class:`asyncworker.http.wrapper.RequestWrapper`; Esse parametro **deve estar tipado**.
- Essa inner function **deve ser** decorada com :py:func:`asyncworker.decorators.wraps()`.

Importante: Não é necessário declarar seu decorator com `(*args, **kwargs)`. O asyncworker vai perceber o parametro que seu decorator precisa e chamará sempre passando apenas os parametros declarados na assinatura.

Um exemplo simples de decorator:

.. code:: python

  from asyncworker.http.wrapper import RequestWrapper
  from asyncworker.decorators import wraps

  def my_handler_decorator(handler):
      @wraps(handler)
      async def _wrapper(wrapper: RequestWrapper):
          # Código principal do decorator vem aqui
          return await call_http_handler(wrapper.http_request, handler)

      return _wrapper

A razão para isso é que o asyncworker permite que um handler receba parametros dinâmicos (:ref:`typed-handlers`) e a função ``call_http_handler()`` é quem tem ciência disso e saberá fazer a resolução correta dos parametros necessários para que o handler seja corretamente chamado.

Esse decorator poderia ser aplicado a um handler assim:


.. code:: python

  @app.http.get(["/"])
  @my_handler_decorator
  async def handler():
    return web.json_response({})


Escrevendo um decorator que precisa conhecer a assinatura original do handler
=============================================================================


Caso o seu decorator precise saber a assinatura original do handler que está sendo decorado, ela pode ser descoberta usando :py:func:`asyncworker.utils.get_handler_original_typehints()`. Essa função deve receber o mesmo parmetro que o ``@wraps()`` recebe. O retorno dessa chamada é o dicionário original que estava no atributo ``__annotations__`` do handler original.

Um exemplo:

.. code-block:: python

    def simple_deco(handler):
        @wraps(handler)
        async def _wrapper():
            return await handler()

        return _wrapper

    def other_deco(handler):
        @wraps(handler)
        async def _wrap():
            return get_handler_original_typehints(handler)

        return _wrap

    @other_deco
    @simple_deco
    async def handler(a: bool, s: str):
          pass


Nesse caso, mesmo o decorator ``@other_deco()`` sendo o decorator no topo da lista de decorators, ele é capaz de retornar a assinatura original.
