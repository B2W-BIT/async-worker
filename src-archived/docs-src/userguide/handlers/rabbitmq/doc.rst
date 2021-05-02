Parametros adicionais para o decorator app.amqp.consume()
---------------------------------------------------------

Para um handler RabbitMQ o decorator ``@app.amqp.consume()`` pode receber alguns parametros adicionais.

  - ``queues``: Lista de filas de onde esse handler receberá mensagens
  - ``vhost``: Indica em qual vhost as filas estatão definidas. Se não passarmos nada será usado ``vhost="/"``
  - ``connection``: Serve para passar manualmente um objeto :py:class:`AMQPConnection <asyncworker.connections.AMQPConnection>` para esse handler. Isso é útil quando sua app se conecta a mais de um broker simultaneamente;
  - ``options``: É uma instância do objeto :py:class:`asyncworker.rabbitmq.AMQPRouteOptions <asyncworker.routes.AMQPRouteOptions>`.

Exemplo de valores para o campo options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _rabbitmq-options:

O objeto :py:class:`AMQPRouteOptions <asyncworker.routes.AMQPRouteOptions>` pode ter os seguintes atributos:

  - ``bulk_size``: Esse valor é um inteiro e diz qual será o tamanho máximo da lista que o handler vai receber, a cada vez que for chamado.
  - ``bulk_flush_interval``: Inteiro e diz o tempo máximo que o bulk de mensagens poderá ficar com tamanho menor do que ``bulk_size``. Exemplo: Se seu handler tem um bulk_size de 4096 mensagens mas você recebe apenas 100 msg/min na fila em alguns momentos seu handler será chamado recebendo uma lista de mensagens **menor** do que 4096.
  - ``connection_fail_callback``: Função assíncrona que é chamada caso haja uma falha durante a conexão com o broker. Essa função recebe a exceção que ocorreu e o número de retentativas que falharam até então. O número de retentativas é zerado quando o app consegue se conectar com o broker.
  - ``on_success``: Diz qual será a ação tomada pelo asyncworker quando uma chamada a um handler for concluída com sucesso, ou seja, o handler não lançar nenhuma exception. O Valor padrão é :py:attr:`Actions.ACK <asyncworker.options.Actions.ACK>`
  - ``on_exception``: Diz qual será a ação padrão quando a chamada a um handler lançar uma excação não tratada. O valor padrão é :py:attr:`Actions.REQUEUE <asyncworker.options.Actions.REQUEUE>`


Exemplo de um código que usa essas opções:

.. code-block:: python

  from asyncworker import App
  from asyncworker.options import Actions
  from asyncworker.rabbitmq.AMQPRouteOptions

  async def fail_handler(e: Exception, n: int):
      print(f"error: {e}, retries {n}")

  @app.amqp.consume(
      ["queue"],
      options=AMQPRouteOptions(
          bulk_size=60,
          bulk_flush_interval=10,
          on_success=Actions.ACK,
          on_exception=Actions.REJECT,
      ),
  )
  async def _handler(messages):
      pass


Consumindo de filas de outros virtualhosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

É possível consumir de filas que estão em outros vistualhosts do mesmo broker. Para isso basta passar o parametro ``vhost`` para do decorator ``@app.amqp.consume()``. Exemplo:


.. code-block:: python

  from asyncworker import App
  from asyncworker.options import Options, Actions, Events
  from asyncworker.rabbitmq.AMQPRouteOptions

  async def fail_handler(e: Exception, n: int):
      print(f"error: {e}, retries {n}")

  @app.amqp.consume(
      ["queue"],
      vhost="logs",
      options=AMQPRouteOptions(
          bulk_size=60,
          bulk_flush_interval=10,
          on_success=Actions.ACK,
          on_exception=Actions.REJECT,
      ),
  )
  async def _handler(messages):
      pass



Nesse caso esse handler consome a fila ``queue`` do virtualhost ``logs``.


Consumindo de filas de brokers diferentes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

É possível consumir, de forma concorrente, de brokers diferentes. Basta que pra isso tenhamos duas conexões distintas e que passemos uma das conexões na hora de regisgtrar nossos handlers. Assim:

.. code-block:: python

  from datetime import datetime
  from typing import List

  from asyncworker import App
  from asyncworker.connections import AMQPConnection
  from asyncworker.http.methods import HTTPMethods
  from asyncworker.options import Actions, Events, Options
  from asyncworker.rabbitmq import RabbitMQMessage, AMQPRouteOptions

  amqp_conn = AMQPConnection(
      hostname="127.0.0.1:5672", username="guest", password="guest", prefetch=1024
  )

  amqp_conn_2 = AMQPConnection(
      hostname="127.0.0.1:5673", username="guest", password="guest", prefetch=128
  )

  app = App(connections=[amqp_conn, amqp_conn_2])


  @app.amqp.consume(["queue"], connection=amqp_conn)
  async def _handler_broker_1(msgs: List[RabbitMQMessage]):
      print(f"Broker 1 ({amqp_conn.hostname}): Recv: {len(msgs)}")


  @app.amqp.consume(["queue"], connection=amqp_conn_2)
  async def _handler_roker_2(msgs: List[RabbitMQMessage]):
      print(f"Broker 2 ({amqp_conn_2.hostname}): Recv: {len(msgs)}")


  @app.run_every(1)
  async def produce(app: App):
      await amqp_conn.put(data={"msg": "Broker 1"}, routing_key="queue")
      await amqp_conn_2.put(data={"msg": "broker 2"}, routing_key="queue")


  app.run()



Uma nota sobre bulk_size e prefetch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

O valor do ``BULK_SIZE`` sempre é escolhido com a fórmula: ``min(BULK_SIZE, PREFRETCH)``. Isso para evitar que o código fique em um deadlock, onde ao mesmo tempo que ele aguarda o bulk encher para poder pegar mais mensagens da fila, ele está aguardando o bulk esvaziar para pegar mais mensagens da fila.


Flush timeout
~~~~~~~~~~~~~~~

Com o flush timeout a ``app`` não necessita ficar presa esperando o bucket encher para conseguir processar as mensagens.
Após o tempo do ``FLUSH_TIMEOUT`` (que são :py:attr:`DefaultValues.BULK_FLUSH_INTERVAL <asyncworker.options.DefaultValues.BULK_FLUSH_INTERVAL>` segundos por default) a ``app`` irá enviar todas as mensagens que já possui para o ``_handler``.
Por exemplo, se tivermos um ``handler`` que possui:

 - Um ``BULK_SIZE`` de 1.000
 - As mensagens para esse handles são publicadas diariamente
 - E o bucket desse handler ficou com 500 mensagens

Nesse caso a ``app`` irá esperar o timeout do flush para liberar essas mensagens para o ``handler``.

Caso queira alterar o tempo default do timeout do flush basta definir env ``ASYNCWORKER_FLUSH_TIMEOUT`` com um número que representará os segundos em que a app irá esperar para realizar o flush.

Também é possível alterar o tempo do timeout do flush definindo o campo ``Options.BULK_FLUSH_INTERVAL`` do dicionário ``options`` passado como parâmetro na criação da rota.
O valor passado para o parametro ``options`` tem precedência sobre a variável de ambiente ``ASYNCWORKER_FLUSH_TIMEOUT``.



Exemplo de um código mais completo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from typing import List
  from asyncworker import App
  from asyncworker.connections import AMQPConnection
  from asyncworker.rabbitmq import RabbitMQMessage, AMQPRouteOptions


  amqp_conn = AMQPConnection(
                host="127.0.0.1",
                user="guest",
                password="guest",
                prefetch_count=256
              )

  app = App(connections=[amqp_conn])


  @app.amqp.consume(
      ["asgard/counts", "asgard/counts/errors"],
      vhost="fluentd",
      options=AMQPRouteOptions(bulk_size=60, bulk_flush_interval=10),
  )
  async def drain_handler(messages: List[RabbitMQMessage]):
      for m in messages:
          print(m)


Nesse exemplo, o handler ``drain_handler()`` recebe mensagens de ambas as filas: ``asgard/counts`` e ``asgard/counts/errors``, que estão no virtualhost ``fluentd``.

Se o handler lançar alguma exception, a mensagem é automaticamente devolvida para a fila (reject com requeue=True);
Se o handler rodar sem erros, a mensagem é automaticamente confirmada (ack).



Escolhendo, individualmente, qual ação será dada a cada mensgem recebida
-------------------------------------------------------------------------

Existem situações onde você precisa que algumas as mensagens recebidas pelo handler teham tratamentos **diferentes** das outras mensagens. Ou seja, nem sempre você quer que todas recebam ``ack`` ou ``requeue``.

Para isso o objeto recebido por um handler (:py:class:`RabbitMQMessage <asyncworker.rabbitmq.message.RabbitMQMessage>`) possui alguns métodos:

.. autoclass:: asyncworker.rabbitmq.message.RabbitMQMessage
  :noindex:
  :members: reject, accept


Opcionalmente, caso seja necessário rejeitar uma mensagem e ao mesmo tempo **não** devolver essa mensagem pra fila,
podemos chamar ``message.reject(requeue=False)``. O valor default do ``requeue`` é ``True``.


Sobre AMQPConnection
---------------------

Esse objeto é o ponto de comunicação principal com um broker RabbitMQ. Aqui temos um método ``put`` onde podemos enviar novas mensagens ao broker.

Essa classe é um modelo pydantic e pode receber alguns parametros no construtor. Esses parametros estão na declaração dessa classe. :py:class:`asyncworker.connections.AMQPConnection`.
