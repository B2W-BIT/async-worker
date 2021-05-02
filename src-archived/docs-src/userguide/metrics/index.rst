Métricas
========

.. versionadded:: 0.15.0
.. _handler-metrics:

O asyncworker permite que seu código exponha métricas customizadas. Cada tipo de métrica expõe uma interface própria e é através dessa interface que é possível controlar o valor dessas métricas.

Cada tipo de métrica (e sua interface) é explicada abaixo.

Os valores de todas as métricas são expostos em formato texto e esse formato é o do `Prometheus <https://prometheus.io/docs/instrumenting/exposition_formats/#text-based-format>`_

Mais detalhes em como esses valores são expostos em sua aplicação podem ser encontrados :ref:`nas configurações de métricas <metrics-config>`.

.. toctree::
   :maxdepth: 5
   :titlesonly:

   config.rst
   types/index.rst
   autoexposed-metrics.rst
   grafana.rst
