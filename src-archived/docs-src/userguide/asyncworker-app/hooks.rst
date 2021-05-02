Hooks de startup e shudtdown
============================

O asyncworker permite que registre eventos para rodarem antes/depois de sua app ser inicializada.

@app.run_on_startup
-------------------

Um cenário bem comum em workers é, por exemplo, a necessidade de se manter e
compartilhar uma conexão persistente com um banco de dados. Em clientes
assíncronos, é comum a necessidade da inicialização de conexões que necessitam
de um loop de eventos rodando. Para esses cenários, usamos o evento de
``on_startup`` da aplicação:

.. code-block:: python

  import aioredis
  from asyncworker import App

  # ...

  @app.run_on_startup
  async def init_redis(app):
      app['redis'] = await aioredis.create_pool('redis://localhost')


  app.run()


@app.run_on_shutdown
--------------------

Assim como o evento de ``on_startup`` sinaliza a inicialização do ciclo de vida
da app, o evento ``on_shutdown`` representa o fim. Um caso de uso comum, é fazer
o processo de finalização de conexões abertas. Como no exemplo anterior
abrimos uma conexão com o `Redis <https://redis.io>`_, utilizando a biblioteca
`aioredis <https://github.com/aio-libs/aioredis>`_, precisamos fechar as conexões
criadas:

.. code-block:: python

  @app.run_on_shutdown
  async def init_redis(app):
      app['redis'].close()
      await app['redis'].wait_closed()
