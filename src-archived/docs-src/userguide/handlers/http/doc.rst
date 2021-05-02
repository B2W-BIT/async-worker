

Registrando um novo handler HTTP
=================================

Todo handler HTTP deve seguir algumas regras:

 - Deve sempre ser decorado com :ref:`@app.http.*() <supported-methods>`
 - Deve declarar seus parametros sempre com definição de tipos, pois é assim que o asyncworker saberá passar :ref:`parametros dinâmicos <handler-path-param>` para o handler.
 - Um handler pode não receber nenhum parâmetro. Para isso basta a assinatura do handler ser vazia.

Alguns objetos já são passados ao handler, caso estejam presentes em sua assinatura.  Eles são:

 - Uma instância de :py:class:`asyncworker.http.wrapper.RequestWrapper`.


Métodos HTTP suportados
=======================

.. _supported-methods:
.. versionadded:: 0.15.2

Para definirmos qual método HTTP nosso handler vai responder, devemos usar um dos decorators que estão disponíveis abaixo de ``app.http.*``. Atualmente temos:

- ``@app.http.get()``
- ``@app.http.post()``
- ``@app.http.put()``
- ``@app.http.patch()``
- ``@app.http.delete()``
- ``@app.http.head()``

Esses decorators recebem como parametro uma lista de paths que serão respondidos pelo handler decorado. Exemplo:

.. code-block:: python


  from aiohttp import web

  from asyncworker import App
  from asyncworker.http.decorators import parse_path
  from asyncworker.http.wrapper import RequestWrapper

  app = App()


  @app.http.get(["/", "/other"])
  async def handler():
      return web.json_response({})


Parametros no path podem ser definidos cercando com ``{}``, ex: ``/users/{user_id}``. Mais delathes em como receber esses valores em seu handler :ref:`aqui <handler-path-param>`.


Usando métodos não suportados pelo asyncworker
==============================================

Eventualmente você pode precisar registrar um handler que responde por um método HTTP que não possui um decorator específico. Nesse caso você pode usar o decorator ``@app.http._route()`` para regisgtrar esse handler.

Mas lembre-se que você está usando uma API interna do asyncworker e que não há garantias de que essa inteface seja mantida estável. O ideal é que o método que você precisa seja adicionado ao projeto.

Um exemplo de handler que usa um método HTTP qualquer:

.. code-block:: python

  @app.http._route(["/bla"], method="CONTINUE")
  async def handler(...):
    pass




ENVs para escolher a porta e o IP onde o server http estará escutando
========================================================================


Por padrão, fazemos o binding em ``127.0.0.1``, porta ``8080``, mas isso pode ser alterado com as envvars ``ASYNCWORKER_HTTP_HOST`` e ``ASYNCWORKER_HTTP_PORT``, respectivamente.



Handlers que são objetos callable
===========================================

.. versionadded:: 0.11.4

É possível também escrever handlers como objetos que são callables, ou seja, possuem o método ``async def __call__()``. Importante notar que a assinatura do método ``__call__()`` segue as mesmas regras da assinatura de uma corotina decorada com o ``@app.route()``.

Esses handlers são especialmente úteis quando você precisa guardar algum tipo de contexto e não quer fazer isso com variáveis globais no nível do módulo.

Um exemplo de um handler:

.. code:: python

  class Handler:
    async def __call__(self, wrapper: RequestWrapper):
      pass


Importante notar que como estamos lidando com um objeto ele precisará ser instanciado antes de ser usado e isso significa que não vamos poder decorá-lo da mesma forma que decoramos handlers que são apenas uma corotina. Um código desse gera erro de sintaxe:

.. code:: python

  class Handler:
    async def __call__(self, wrapper: RequestWrapper):
      pass

  h = Handler()

  @app.http.get(...)
  h

Por isso esses handlers precisam ser registrados chamando o decorator manualmente, assim:

.. code:: python

  class Handler:
    async def __call__(self, wrapper: RequestWrapper):
      pass

  h = Handler()

  app.http.get(...)(h)


.. _typed-handlers:

Handlers que recebem mais do que apenas Request
================================================

.. versionadded:: 0.11.0

O asyncworker permite que um handler receba quaisquer prametros. Para isso a assinatura do handler deve conter typehints em todos os parametros. Isso faz com que o asyncworker consiga fazer a resolução desses prametros e consiga chamar o handler corretamente.

O wrapper que é passado ao handler (:py:class:`asyncworker.http.wrapper.RequestWrapper`) possui um atributo chamado ``types_registry`` que é do tipo :py:class:`asyncworker.types.registry.TypesRegistry`. Para que um parametro possa ser passado a um handler ele deve ser adicionado a esse registry.

Um exemplo de como popular esse registry é através de um decorator aplicado diretamente ao um handler. Vejamos um exemplo:

.. code:: python


  from aiohttp import web
  from myproject.models.user import User
  from http import HTTPStatus
  from asyncworker.decorators import wraps
  from asyncworker.http.wrapper import RequestWrapper


  def auth_required(handler):
      @wraps(handler)
      async def _wrapper(wrapper: RequestWrapper):
          basic_auth = wrapper.http_request.headers.get("Authorization")
          user = get_authenticated_user(basic_auth)
          if not user:
              return web.json_response({...}, status=HTTPStatus.UNAUTHORIZED)

          wrapper.types_registry.set(user)
          return await call_http_handler(wrapper.http_request, handler)

      return _wrapper

  @app.http.get(["/"])
  @auth_required
  async def handler(user: User):
      return web.json_response({})

Aqui o decorator ``auth_required()`` é responsável por fazer a autenticação, pegando dados do Request e encontrando um usuário válido. Se um usuário não puder ser encontrado, retorna ``HTTPStatus.UNAUTHORIZED``. Se um usuário autenticar com sucesso, apenas adiciona o objeto user (que é do tipo ``User``) no registry que está no ``RequestWrapper``. Isso é o suficiente para que o handler, quando for chamado, receba diretamente esse user já autenticado.

Typehints que extraem dados do Request
--------------------------------------

.. versionadded:: 0.19.1

O Asyncworker fornece alguns typehints que são inteligentes o bastante para extrairem dados do request e passar esses dados para o handler sendo chamado.

Todos os typhints são genéricos e recebem apenas **um** parametro. Os typehitns disponíveis são:

- ``PathParam[T]``

Onde ``T`` é o tipo do dado que será extraído do request. Para usar esses typehints basta anotar os parametros do seu handler com o tipo necessário. Como o seu handler passará a receber um argumento do tipo ``PathParam`` (ou qualquer outro typehint inteligente) será necessáio, de alguma forma, extrair o valor real de dentro desse objeto.

Todos os typehints fornecidos pelo asyncworker possuem o método ``unpack()``. Esse  método serve justamente para extrair o valor que foi lido do request.

Note que esse método é uma corotina. Ser corotina permite que o asyncworker faça "lazy parsing" do request. Isso significa que, em alguns casos, o request só será efetivamente lido quando você chamar ``await unpack()``. Isso é especialmente útil quando falamos de Request Bodies que são grandes.

Receber uma instância da classe mencionada na assinatura do handler (em vez de receber diretamente o valor vindo do request) permite que o seu código seja validado estaticamente de forma correta.

Aqui tem um exemplo simples de como usar o :ref:`PathParam[T] <handler-path-param>`.

Recebendo parâmetros vindos do path do Request
-----------------------------------------------

.. _handler-path-param:
.. versionadded:: 0.19.1

É possível receber em seu handler parametros definidos no path da requisição. Isso é feito través do typehint :py:class:`asyncworker.http.types.PathParam`.

Quando um handler menciona esse tipo em seus parametros isso faz o asyncworker tentar extrair parametros do path e passar para o handler.

Importante notar que, primeiro o asyncworker vai procurar nosso parametro pelo nome e só depois tentará procurar o tipo.  Exemplo:

.. code-block:: python

  from asyncworker.http.types import PathParam

  @app.http.get(["/by_id/{_id}"])
  async def by_id(_id: PathParam[int]):
      value = await _id.unpack()
      return web.json_response({"_id": value})

Nesse caso, como handler está dizendo que precisa de um parametro chamado ``_id`` temos que declarar um parametro de mesmo nome no path da Request. Depois que esse `match` for feito passaremos o valor recebido no path para o construtor do tipo definido na assinatura do handler, nesse caso ``PathParam``.

Para que seja possível lidar bem com linters (tipo ``mypy``) o que o asyncworker faz é de fato chamar o handler passando uma instância de ``PathParam``. Essa intância tem, internamente, o valor real que foi passdo no path do request, já convertido para o tipo correto. Nesse caso aqui um ``int``.

Importante notar que só serão passados ao handler os parametros que estão definidos na assinatura. Então se seu path recebe dois parametros e seu handler só se interessa por um deles, basta declarar na assinatura do handler o parametro que você quer receber.

Esse typehint pode receber qualquer tipo primitvo do python: ``int``, ``float``, ``bool``. Quando recebe ``bool`` valem as regras do `Pydantic <https://pydantic-docs.helpmanual.io/usage/types/#booleans>`_.
