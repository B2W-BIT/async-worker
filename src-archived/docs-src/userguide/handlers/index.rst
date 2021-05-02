
Tipos de Handlers
=================

.. _handler-types:

O asyncworker suporta alguns tipos de handlers diferentes. Por handler entende-se a
função que será chamada quando um estímulo externo chegar. Cada Handler pode ser registrado
em apenas **uma** origem de eventos. Por exemplo, não podemos te um mesmo handler que é chamado por causa de um Request HTTP e ao mesmo tempo ser chamado por causa da uma nova mensagem me uma fila.

Isso porque os parametros do handler mudam de acordo com a origem de seus eventos.
Um handler RabbitMQ recebe, por exemplo, uma lista de mensagens. Um Handler HTTP recebe uma cópia do Request.

Abaixo você poderá ver em detalhes cada um desses handlers e como criar cada um deles.

.. toctree::
   :maxdepth: 3
   :titlesonly:

   http/index.rst
   rabbitmq/index.rst


Métricas
--------

Mais detalhes em como expor suas próprias métricas você poderá ver na documentação sobre :ref:`métricas <handler-metrics>`.
