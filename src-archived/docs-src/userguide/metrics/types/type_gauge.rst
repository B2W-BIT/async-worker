Gauge
=====

.. _metric-type-gauge:

O tipo Gauge é usado para acompanhar a "velocidde instantânea" de uma métrica, ou seja, seu valor atual. Esse valor pode variar tanto pra cima como pra baixo.

É útil também para acompanhar duração de execução de tarefas.



Interface principal
-------------------

A interface principal são os métodos ``inc()``, ``dec()`` e ``set()``.

.. code:: python

  from asyncworker.metrics import Gauge

  g = Gauge("temperatura_atual", "Mostra a temperatura atual do sensor")

  g.inc()  # Incrementa o valor em 1
  g.dec(20) # Decrementa o valor em 20
  g.set(8.9) # Força o valor a ser 8.9


Interfaces adicionais
---------------------

Algumas interfaces adicionais também são expostas para facilitar o uso, são elas:


track_inprogress()
~~~~~~~~~~~~~~~~~~

Essa interface serve para já incrementar e decrementar de forma automática. Pode ser usada como um decorator ou como context manager. Útil para controlar contagens que só fazem sentido durante a execução de algum código.

.. code:: python

  from asyncworker.metrics import Gauge

  g = Gauge("envio_de_emails_em_andamento", "Quantidade de emails sendo enviados")

  @g.track_inprogress()
  def envia_email(...)
    pass

Nesse caso a métrica será incrementada quando a função ``envia_email()`` for chamada e decrementada quando a função terminar de rodar.

.. code:: python

  from asyncworker.metrics import Gauge

  g = Gauge("queries_em_andamento", "Quantidade de queries sendo feitas")


  with g.track_inprogress():
    await db.query(...)

Nesse caso a métrica será incrementada no início do context e decrementada quando o context terminar.


time()
~~~~~~~

Essa interface é útil para contar tempo, duração de alguma coisa.

.. code:: python

  from asyncworker.metrics import Gauge

  g = Gauge("query_duration", "Duração das queries no banco")

  @g.time()
  def run_query(...)
    pass

  with g.time();
    run_query(...)


Nesses dois exemplos a métrica ``query_duration`` marcará o tempo de execução da função ``run_query()``.
