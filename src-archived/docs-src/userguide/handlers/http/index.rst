HTTP
====

.. versionadded:: 0.6.0

Aqui mostraremos como escrever um handler que é estimulado através de requisições HTTP.


Um handler é simplesmete uma corotina que recebe um request wrapper (:py:class:`asyncworker.http.wrapper.RequestWrapper`) e retorna uma response (``aiohttp.web.Response``). Essa corotina passa a ser um handler "asyncworker" quando é decorada com :ref:`@app.http.*() <supported-methods>`, onde ``app`` é uma instância de ``asyncworker.App``.

Vejamos um handler bem simples que apenas retorna ``HTTP 200 OK``.

.. code:: python

  from aiohttp import web

  from asyncworker.http.wrapper import RequestWrapper
  from asyncworker import App

  app = App()


  @app.http.get(["/"])
  async def one_param(wrapper: RequestWrapper):
      return web.json_response({})


O ``RequestWrapper`` tem um atributo ``.http_request`` que é o Request original entregue pelo ``aiohttp``.
Podemos fazer o que for preciso para extrair dele as informações que precisarmos. Para mais detalhes, veja a doc do aiohttp: https://docs.aiohttp.org/en/stable/web.html


.. toctree::
   :maxdepth: 5

   doc.rst
   exposed-metrics.rst
