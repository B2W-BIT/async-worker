Métricas expostas para aplicações RabbitMQ
==============================================

.. versionadded:: 0.15.0

Essas são as métricas expostas automaticamente para todas as aplicações RabbitMQ.


- ``amqp_active_consumers``
    Total atual de consumers ativos
- ``amqp_processed_messages``
    labels: ("queue_name", "action")

    Quantidade de mensagens processadas separadas por fila de origem (``queue_name``) e ``action`` (ack, reject e requeue)

- ``amqp_active_connections``
    Quantidade de conexões ativas com o Broker

- ``amqp_filled_buckets``
    Quantidade de vezes que o bucket interno (para processamento em lote) ficou cheio. Mais detalhes: :ref:`BULK_SIZE <rabbitmq-options>`.

- ``amqp_flushed_buckets``
    Quantidade de vezes que o bucket foi esvaziado e teve suas mensagens entregues ao handler. Mais detalhes: :ref:`BULK_FLUSH_INTERVAL <rabbitmq-options>`
    O bucket é esvaziado se seu tamanho limite (``BULK SIZE``) é atingido ou se o tempo máximo é antingido (``BULK_FLUSH_INTERVAL``).

- ``amqp_bucket_handle``
    buckets :py:class:`settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS <asyncworker.conf.Settings>`.

    Histograma contendoo tempo gasto em cada chamada ao handler.
