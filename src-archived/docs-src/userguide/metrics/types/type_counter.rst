Counter
=======

Tipo contador serve para acompanhar contagens de itens. Esse tipo só pode ser incrementado com valores **positivos**. Caso você precise acompanhar um valor que pode aumentar e diminuir use o tipo :ref:`Gauge <metric-type-gauge>`.

Exemplo de uso
---------------

.. code:: python

  from asyncworker.metrics import Counter

  c = Counter("users_created", "Total de Usuários criados no sistema")
  c.inc()  # Incrementa o contados em 1
  c.inc(3) # Incrementa o contados em 3


Interface principal
-------------------

A interface principal desse tipo de Métrica é o método ``inc()``. Através dele é que mudamos o valor interno de uma métrica.

.. code:: python

  def inc(value=1):
    pass

O método ``inc()`` não pode receber valores negativos.


Interfaces adicionais
~~~~~~~~~~~~~~~~~~~~~

Esse tipo de métrica expõe uma interface adicional que é o método ``count_exceptions()``. Esse método pode ser usado com decorator ou como context manager.

Por padrão conta todas as exceções, exemplo:

.. code:: python

  from asyncworker.metrics import Counter
  c = Counter("erros", "Total de erros")

  @c.count_exceptions()
  def f():
    pass

  with c.count_exceptions():
    pass


Se desejar contar apenas um tipo de exceção específico, basta passar esse tipo como parametro.

.. code:: python

  # Count only one type of exception
  with c.count_exceptions(ValueError):
    pass
