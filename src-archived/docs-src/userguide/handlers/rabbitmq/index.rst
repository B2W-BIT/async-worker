RabbitMQ
=========

Aqui você verá como escrever um handler que recebe mensagens de um broker RabbitMQ


Todo handler desse tipo recebe o mesmo parametro, que é uma lista de objetos :py:class:`asyncworker.rabbitmq.message.RabbitMQMessage`.


Isso significa que a assinatura dos seus handlers são fixas, ou seja, todos eles possuem essa assinatura:

.. code-block:: python

  from asyncworker.rabbitmq.message import RabbitMQMessage
  from typing import List

  async def handler(msgs: List[RabbitMQMessage]):
    ...


Como no caso de handlers RabitMQ é preciso ter uma conexão prévia com o servidor de filas, precisamos criar uma instância de :py:class:`asyncworker.connections.AMQPConnection`. Essa instância deve ser passada no momento da criação de sua :ref:`Asyncworker App <asyncworker-app>`.

Essa instância de conexão pode também ser usada dentro do handler, caso necessário.


Um exemplo disso é quando precisamos de um handler que lê mensagens de um fila e publica em outra. Esse exemplo pode ser escrito assim:

.. code-block:: python

  from typing import List

  from asyncworker import App
  from asyncworker.connections import AMQPConnection
  from asyncworker.rabbitmq import RabbitMQMessage

  amqp_conn = AMQPConnection(
                hostname="127.0.0.1",
                username="guest",
                password="guest",
                prefetch_count=256
              )

  app = App(connections=[amqp_conn])


  @app.amqp.consume(["original_queue"])
  async def handler(messages: List[RabbitMQMessage]):
      await amqp_conn.put(
          data={"dogs": ["Xablau", "Xena"]},
          exchange="ANOTHER_EXCHANGE",
          routing_key="another-routing-key"
      )


se a fila de destino estiver um outro virtual host, basta pegar uma nova conexão com esse virtual host acessando o atributo (dict like) com o nome do virtual host desejado, no objeto da conexão, assim:

.. code-block:: python


  @app.amqp.consume(["original_queue"])
  async def handler(messages: List[RabbitMQMessage]):
      await amqp_conn["other-vhost"].put(
          data={"dogs": ["Xablau", "Xena"]},
          exchange="ANOTHER_EXCHANGE",
          routing_key="another-routing-key"
      )

.. toctree::
   :maxdepth: 5
   :titlesonly:

   doc.rst
