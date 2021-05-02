Compartilhamento de dados e inicializações assíncronas
==========================================================

Recomendamos que com o ``asyncworker`` você não utilize variáveis globais e que
utilize o estado do ``asyncworker.App`` para manter os seus
`singletons <https://pt.wikipedia.org/wiki/Singleton>`_. Para isso, o ``asyncworker.App``
disponibiliza _hooks_ para que códigos sejam injetados ao longo ciclo de vida
da aplicação, tornando possível a manutenção, manipulação e compartilhamento de
estado pelos handlers.

Armazenando na App
-------------------

Para armazenar estados globais da aplicação, podemos utilizar a instância de
``asyncworker.App``, que age como um dicionário.


.. code-block:: python

  app['processed_messages'] = 0

Então você poderá utilizá-los nos seus handlers

.. code-block:: python

  @app.route(routes=["words_to_index"], type=RouteTypes.AMQP_RABBITMQ)
  async def drain_handler(messages):
      app['processed_messages'] += 1

**Obs.:** Vale lembrar que esse dicionário é compartilhado ao longo de toda app
e utilizado inclusive pelo próprio asyncworker, então uma boa prática é escolher
nomes únicos para evitar conflitos.
