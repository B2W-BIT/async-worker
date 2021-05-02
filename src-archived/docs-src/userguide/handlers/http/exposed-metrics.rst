Métricas expostas para aplicações HTTP
==========================================


.. versionadded:: 0.15.1

Aqui estão descritas todas as métricas automaticamente expostas para qualquer aplicação asyncworker HTTP.


- ``http_request_duration_seconds``
    Histograma que mede o tempo (em segundos) de cada request HTTP processada e
    distribui essas ocorrências nos buckets configurados.

    Com essa métrica, podemos medir a duração de requests HTTP com percentis ou médias.
    Não é recomendado que você confie nas médias para determinar a saúde da sua aplicação,
    já que elas podem te enganar e mascarar o real estado da sua aplicação.

    - labels
        - ``method``: Método usado no request
        - ``path``: Path do request
        - ``status``: Status code retornado, mesmo quando já uma exception.

    - ``buckets`` :py:class:`settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS <asyncworker.conf.Settings>`


- ``http_requests_in_progress``
    Gauge que representa a quantidade de requests HTTP sendo processadas no momento

    - labels
        - ``method``: Método usado no request
        - ``path``: Path do request

- ``http_response_size_bytes``
    Histograma que mede o tamanho em bytes das respostas para requests HTTP

    - labels
        - ``method``: Método usado no request
        - ``path``: Path do request