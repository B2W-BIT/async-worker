Configurando exposição de Métricas
==================================

.. _metrics-config:


Todas as métricas expostas por uma aplicação asyncworker podem ser lidas através de um endpoint HTTP. A porta onde esse endpoint é servido é a mesma porta da sua app HTTP (caso esteja usando uma) e por padrão é o valor da config :py:class:`settings.HTTP_PORT <asyncworker.conf.Settings>`

O path padrão desse endpoint é :py:class:`settings.METRICS_ROUTE_PATH <asyncworker.conf.Settings>`.

:ref:`Por padrão o endpoint que expõe as métricas já é ativado <asyncworker-auto-metrics>`. Caso queira desligar esse endpoint isso pode ser feito pela envvar ``ASYNCWORKER_METRICS_ROUTE_ENABLED=0``.


Formação do nome das métricas
-----------------------------

Todas as métricas expostas por uma aplicação asyncworker possuem um prefixo. Esse prefixo é ``asyncworker_``. Isso significa que se sua métrica é declarada com o nome ``users_total`` ela será exposta com nome ``asyncworker_users_total``.

Isso é útil para que suas métricas não se confundam com todas as outras métricas do seu sistema, incluindo métricas de outras aplicações.

Caso você precise de métrica com nomes diferentes **por aplicação** é possível adicionar um prefixo a todas as métricas expostas pela sua app. Isso inclui também o nome de quaisquer das métricas expostas pelo próprio asyncworker (por enquando, nenhuma).

Para isso basta usar a ENV ``ASYNCWORKER_METRICS_APPPREFIX`` e colocar nela o valor que você quiser. Exemplo:

Se no seu código você declarou uma métrica de nome ``msg_processed`` e rodou sua app com a ENV ``ASYNCWORKER_METRICS_APPPREFIX=myapp``. Essa métrica será exposta com o nome ``asyncworker_myapp_msg_processed``.

Por padrão esse prefixo tem valor vazio.
