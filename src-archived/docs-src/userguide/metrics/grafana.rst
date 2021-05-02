Integração com Grafana
======================

Importando um dashboard
-----------------------

1. No menu lateral, clique em ``+``
2. Selecione ``Import``
3. Cole a URL ou o identificar do dashboard e clique em ``Load``
4. Selecione o datasource e clique em ``Import``

Dashboards oficiais
-------------------

- `Asyncworker HTTP Routes <https://grafana.com/grafana/dashboards/14246>`_: Visualizações detalhadas e customizáveis de métricas HTTP, expostas automaticamente em aplicações async-worker como tempo de resposta de requisições, throughput, tamanho em bytes de respostas, taxa de erros e muito mais.

.. image:: https://grafana.com/api/dashboards/14246/images/10230/image

- `Asyncworker Python Process <https://grafana.com/grafana/dashboards/14245>`_: Visualizações de métricas relacionadas ao processo python e usos de recurso como CPU, RAM, Garbage Collection, file descriptors e outras informações expostas automaticamente em aplicações async-worker.

.. image:: https://grafana.com/api/dashboards/14245/images/10229/image

Exemplos
--------

- `Visualização de métricas do Asyncworker com Grafana e Prometheus <https://github.com/b2wdigital/async-worker/tree/master/examples/docker-compose-asyncworker-with-metrics>`_

