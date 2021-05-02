Histograma
==========

O tipo Histigrama serve para observar a quantidade de vezes que um evento ocorreu e categorizar essa quantidade em intervalos chamados `buckets`.

Um métrica histograma sempre tem buckets definidos. O valor padrão para essa métrica em aplicações asyncworker é :py:class:`settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS <asyncworker.conf.Settings>`.

Você pode escolher seus próprios buckets passando um parametro nomeado no construtor da métrica. Esse parametro é o ``buckets`` e é uma lista de ``float``.

.. code:: python

  from asyncworker.metrics import Histogram

  h = Histogram("users_age", "Idade dos usuários logados", buckets=[20.0, 30.0, 40.0, float("inf")])

  h.observe(25)
  h.observe(49)
  h.observe(19)

Sempre que você entrega um novo valor para essa métrica ela vai categorizar esse valor dentro das divisões dos buckets. Olhando essa execução acima teremos as seguintes métrias sendo geradas no output:

.. code:: text

   asyncworker_users_age_bucket{le="20.0"} 0.0
   asyncworker_users_age_bucket{le="30.0"} 2.0
   asyncworker_users_age_bucket{le="40.0"} 2.0
   asyncworker_users_age_bucket{le="+Inf"} 3.0
   asyncworker_users_age_count 3.0
   asyncworker_users_age_sum 93.0
   asyncworker_users_age_created 1589816720.090581

Nesse exemplo tivemos 3 observações dessa métrica, por isso a metrica ``asyncworker_users_count`` tem valor `3.0`. Cada observação somou um ao valor do intervalo correspondente.

- Nenhum valor é menor que ``20`` por isso a métrica ``asyncworker_users_age_bucket{le="20.0"}`` tem valor ``0.0``
- Dois valores são ao mesmo tempo menores que ``20`` e ``30``. São eles: ``19`` e ``25``. Por isso as métricas possuem valor ``2.0``
- Todos os valores observados são menores que ``+Inf`` e por isso essa merica possui valor ``3.0``.

Interface principal
--------------------

A interface principal dessa métrica é o método ``observe()``. Esse método pode receber qualquer valor.

Interfaces adicionais
----------------------

time()
~~~~~~~

O método ``time()`` serve para marcar o tempo de algo e passar esse tempo para o ``observe()``. Ele pode ser usado tanto como decorator como contextmanager.
