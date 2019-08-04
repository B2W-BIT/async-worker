HTTP
====


Aqui mostraremos como escrever um handler que é estimulado através de requisições HTTP.


Um handler é simplesmete uma corotina que recebe um request (``aiohttp.web.Request``) e retorna uma response (``aiohttp.web.Response``). Essa corotina passa a ser um handler "asyncworker" quando é decorada com ``@app.route()``, onde ``app`` é uma instância de ``asyncworker.App``.

Vejamos um handler bem simples que apenas retorna ``HTTP 200 OK``.

.. code:: python

  @app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
  async def handler(req: web.Request):
    return web.json_response({})


Como recebemos um request do aiohttp, podemos fazer o que for preciso para extrair dele as informações que precisarmos. Para mais detalhes, veja a doc do aiohttp: https://docs.aiohttp.org/en/stable/web.html


Aplicando decorators customizados a um handler
----------------------------------------------

É possível escrever seus próprios decorators e aplicá-los a seus handlers, junto com o decorator ``@app.route``. No entando temos algumas regras:

- O decorator ``@app.route()`` deve estar sempre no topo da lista de decorators de um handler;
- Os decorators intermediários devem sempre usar a função :py:func:`asyncworker.routes.call_http_handler()` no momento de chamar o objeto que estão decorando;
- A inner function retornada pelo decorator deve ser uma corotina;
- A inner function deve receber apenas ``aiohttp.web.Request``;
- Essa inner function não deve ser decorada com ``@functools.wraps()``.


Um exemplo simples de decorator:

.. code:: python


  def my_handler_decorator(handler):
      async def _wrapper(request: web.Request):
          # Código principal do decorator vem aqui
          return await call_http_handler(request, handler)

      return _wrapper

A razão para isso é que o asyncworker permite que um handler receba parametros dinâmicos (mais sobre isso adiante) e a função ``call_http_handler()`` é quem tem ciência disso e saberá fazer a resolução correta dos parametros necessários para que o handler seja corretamente chamado.

Esse decorator poderia ser aplicado a um handler assim:


.. code:: python

  @app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
  @my_handler_decorator
  async def handler(req: web.Request):
    return web.json_response({})


Handlers que recebem mais do que apenas Request
-----------------------------------------------

O asyncworker (``0.10.1+``) permite que um handler receba quaisquer prametros. Para isso a assinatura do handler deve conter typehints em todos os parametros. Isso faz com que o asyncowker consiga fazer a resolução desses prametros e consiga chamar o handler corretamente.

Todas as instancias de ``aiohttp.web.Request`` recebem um atributo chamado ``types_registry`` que é do tipo :py:class:`asyncworker.types.registry.TypesRegistry`. Para que um parametro possa ser passado a um handler ele deve ser adicionado a esse registry do request.

Um exemplo de como popular esse registry é através de um decorator aplicado diretamente ao um handler. Vejamos um exemplo:

.. code:: python


  from aiohttp import web
  from myproject.models.user import User
  from http import HTTPStatus


  def auth_required(handler):
      async def _wrapper(request: web.Request):
          basic_auth = request.headers.get("Authorization")
          user = get_authenticated_user(basic_auth)
          if not user:
              return web.json_response({...}, status=HTTPStatus.UNAUTHORIZED)

          request["types_registry"].set(user)
          return await call_http_handler(request, handler)

      return _wrapper

  @app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
  @auth_required
  async def handler(user: User):
      return web.json_response({})

Aqui o decorator ``auth_required()`` é responsável por fazer a autenticação, pegando dados do Request e encontrando um usuário válido. Se um usuário não puder ser encontrado, retorna ``HTTPStatus.UNAUTHORIZED``. Se um usuário autenticar com sucesso, apenas adiciona o objeto user (que é do tipo ``User``) no registry que está no request. Isso é o suficiente para que o handler, quando for chamado, receba diretamente esse user já autenticado.
