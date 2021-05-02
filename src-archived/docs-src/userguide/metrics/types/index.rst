Tipos de Métricas
=================

Abaixo estão listdos todos os tipos de métricass suportados pelo asyncworker.


Nota sobre corotinas
---------------------

Todas as métricas que expõem interfaces via decorators não podem ser usadas para decorar corotinas. Isso será resolvido no futuro.

Uso geral dos tipos de métricas
--------------------------------

Os campos obrigatórios de uma métrica são:

 - nome
 - documentação

Esses valores são passados no construtor da métrica. Dessa forma:

.. code:: python

  from asyncworker.metrics import Gauge

  g = Gauge(<nome>, <documentação>)

Se a sua métrica possui labels os nomes das labels podem ser passados no parametro nomeado ``labelnames``, assim:

.. code:: python


  from asyncworker.metrics import Gauge

  g = Gauge(<nome>, <documentação>, labelnames=["label1", "label2", ...])

Como usar labels
~~~~~~~~~~~~~~~~~


Quando sua métrica faz uso de labels é necessário passar o valor dessas labels no momento em que o valor da métrica é passado. Isso é feito através do método ``labels()``, dessa forma:


.. code:: python


  from asyncworker.metrics import Gauge

  g = Gauge(<nome>, <documentação>, labelnames=["label1", "label2", ...])

  g.labels(label1="valor", labels2=10).inc()


O método ``labels()`` pode ser encadeado com o uso das interfaces expostas como contextmanager ou decorator.

Tipos de métricas disponibilizadas pelo asyncworker
-----------------------------------------------------

Cada tipo de métrica possui sua própria interface que está documentada em sua respectiva página, listadas a seguir:

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :glob:

   type_*
