Escrevendo Testes Unitários
===========================


Por causa :ref:`da incompatibilidade com múltiplos loops <incompat>` para escrever testes você precisa ter certeza que seu test runner não está criando novos loops para cada um dos casos de teste sendo rodados. Por padrão o `asynctest <https://github.com/Martiusweb/asynctest>`_ faz isso. No caso do asynctest, basta adicionar um atributo ``use_default_loop = True`` (doc `aqui <https://asynctest.readthedocs.io/en/latest/asynctest.case.html#asynctest.TestCase.use_default_loop>`_) em sua classe de teste.


Usando um HTTP test client para testar rotas HTTP
--------------------------------------------------

Quando estamos testando uma app HTTP é bem útil podermos fazer uma requisição real paa rotas dessa app. Para isso o asyncworker dispõe de um TestClient.

Instanciando com ContextManager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Esse TestClient recebe como parametro a instância de sua :py:class:`App <asyncworker.app.App>`, que é onde estão definidas as rotas. Esse TestClient é conseguido através de um contextmanager, usando a classe :py:class:`asyncworker.testing.HttpClientContext`.

.. code:: python

  class HTTPAppTest(TestCase):
      async def setUp(self):
          self.app = App()

          @self.app.route(
              ["/param"], type=RouteTypes.HTTP, methods=["GET"]
          )
          @parse_path
          async def path_multiple_params():
              return web.json_response({})

      async def test_make_http_request(self):
          async with HttpClientContext(self.app) as client:
              resp = await client.post("/get_by_id/42")
              self.assertEqual(200, resp.status)

essa forma é útil quando você precisa testar características que podem ser comprovadas em qualquer app asyncworker e por isso você declara uma nova app em cada caso de teste.

Instanciando com decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se você estiver testando uma app principal que já está toda declaradad e não precisará mudar durante os testes é possível decorar seus casos de teste com :py:func:`asyncworker.testing.http_client`.


.. code:: python

  app = App()


  @app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
  async def _h():
      return web.json_response({})


  class HttpClientTestCaseDecoratorTest(TestCase):
      @http_client(app)
      async def test_can_decorate_method(self, client):
          resp = await client.get("/")
          self.assertEqual(HTTPStatus.OK, resp.status)
