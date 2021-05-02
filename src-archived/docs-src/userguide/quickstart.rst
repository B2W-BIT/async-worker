Início rápido
=============

Um exemplo rápido para mostrar a ideia geral do asynworker.

.. code:: python

  from asyncworker import App
  from asyncworker.http.wrapper import RequestWrapper


  app = App()

  @app.http.get(["/"])
  async def handler(wrapper: RequestWrapper):
    return web.json_response({})

Esse código é possível ser rodado na linha de comando e é capaz de atendar a uma requisição HTTP assim:

.. code:: shell

  curl http://127.0.0.1:8080/


Consumindo de uma fila no RabbitMQ
----------------------------------

.. code:: python


   from asyncworker import App
   from asyncworker.connections import AMQPConnection


   amqp_conn = AMQPConnection(host="127.0.0.1", user="guest", password="guest", prefetch_count=256)
   app = App(connections=[amqp_conn])

   @app.amqp.consume(["asgard/counts", "asgard/counts/errors"],
              vhost="fluentd")
   async def drain_handler(message):
       print(message)

Nesse exemplo, o handler ``drain_handler()`` recebe mensagens de ambas
as filas: ``asgard/counts`` e ``asgard/counts/errors``, que estão no virtualhost ``fluentd``.

Se o handler lançar alguma exception, a mensagem é automaticamente
devolvida para a fila (reject com requeue=True); Se o handler rodar sem
erros, a mensagem é automaticamente confirmada (ack).


Lendo dados de um endpoint Server Side Events
---------------------------------------------

.. code:: python

   import json
   from asyncworker import App, RouteTypes, Options
   from asyncworker.connections import SSEConnection


   sse_conn = SSEConnection(url="http://172.18.0.31:8080/")
   app = App(connections=[sse_conn])

   @app.route(["/v2/events"], type=RouteTypes.SSE, options={Options.BULK_SIZE: 2})
   async def _on_event(events):
       event_names = [e.name for e in events]
       print(f"Events received: {len(events)} {event_names}")
       for event in events:
           data = ""
           if event.name == 'deployment_info':
               data = event.body['plan']['id']
           if event.name == 'deployment_success':
               data = event.body['id']
           if event.name == 'status_update_event':
               data = f"app={event.body['appId']}, task={event.body['taskId']} ({event.body['taskStatus']})"

           print(f"Event Received: {event.name} {data}")

Nesse exemplo, o handler ``_on_event()`` recebe os eventos enviados pelo
servidor. O objeto ``events`` é sempre uma lista, mesmo quando estamos
usando ``BULK_SIZE=1`` (Falaremos sobre isso mais a frente)


Recebendo dados através de requisições HTTP
-------------------------------------------

.. code:: python

   from asyncworker import App
   from asynworker.http.wrapper import RequestWrapper

   # ...

   @app.http.get(routes=['/', '/hello'])
   async def index(wrapper: RequestWrapper) -> web.Response:
       return web.Response(body="Hello world")

Nesse exemplo, declaramos um handler ``index``, que receberá uma
instância de :py:class:`asyncworker.http.wrapper.RequestWrapper` para cada acesso às rotas ``GET /``
e ``GET /hello``.


Rodando seu worker
------------------

Ambos os exemplos precisam de um ``main()`` para poderem rodar. Um
exemplo de ``main`` seria o seguinte, assumindo que o objeto ``app``
está no módulo ``myworker``:

.. code:: python


   from myworker import app

   app.run()

Nesse ponto sua app já estará rodando e caso você seja desconectado, um
loop ficará tentanto reconectar. A cada erro de conexão um log de
exception é gerado.

No momento que você roda esse código (``app.run()``) todos os seus handlers registrados começam a funcionar.
