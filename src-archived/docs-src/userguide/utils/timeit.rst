Timeit
======

.. versionadded:: 0.3.0

Gerenciador de contexto
-----------------------

Um gerenciador de contexto para marcar o tempo de execução de código e chamar um callback ``Callable[..., Coroutine]`` assíncrono ao final, com o tempo total de execução.

.. code-block:: python

  import asyncio
  from asyncworker.utils import Timeit


  async def log_callback(**kwargs):
      print(kwargs)
      # >>> {'transactions': {'xablau': 1.0028090476989746}, 'exc_type': None, 'exc_val': None, 'exc_tb': None}


  async def main():
      async with Timeit(name="xablau", callback=log_callback):
          await asyncio.sleep(1)

  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())

Caso uma exceção seja levantada dentro do contexto, ``log_callback`` será chamado com os dados da exceção explicitamente.


.. code-block:: python

  import asyncio
  from asyncworker.utils import Timeit


  async def log_callback(**kwargs):
      print(kwargs)
      # >>> {'transactions': {'xablau': 3.0994415283203125e-06}, 'exc_type': <class 'KeyError'>, 'exc_val': KeyError('error',), 'exc_tb': <traceback object at 0x10c10c7c8>}


  async def main():
      async with Timeit(name="xablau", callback=log_callback):
          raise KeyError("error")

  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())

Decorator
---------

Também é possível utilizar `Timeit` como um decorator:

.. code-block:: python

  # ...

  @app.route(["xablau-queue"], type=RouteTypes.AMQP_RABBITMQ, vhost="/")
  @Timeit(name="xablau-access-time", callback=log_callback)
  async def drain_handler(message):
      await access_some_remote_content()

Múltiplas transações
--------------------

.. versionadded:: 0.4.0

Muitas vezes queremos ter várias métricas ao mesmo tempo para contar o tempo
dentro de um mesmo contexto de execução. Para isso, uma mesma instância pode
receber múltiplas chamadas.

.. code-block:: python

  async def printit(**kwargs):
      print(kwargs)
      # >>> {'transactions': {'c': 0.10274815559387207, 'b': 0.20585179328918457, 'a': 0.3061490058898926}, 'exc_type': None, 'exc_val': None, 'exc_tb': None}


  async def foo():
      async with Timeit(name='a', callback=printit) as timeit:
          await asyncio.sleep(.1)
          async with timeit(name='b'):
              await asyncio.sleep(.1)
              async with timeit(name='c'):
                  await asyncio.sleep(.1)
