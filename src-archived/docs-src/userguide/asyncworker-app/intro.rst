.. _asyncworker-app:

Sobre a classe principal App
============================

Todo código do asyncworker começa com uma instância de :py:class:`asyncworker.app.App`. Esse é o objeto onde declaramos as "rotas" da sua aplicação e é também onde chamamos o método ``run()``, que é quem efetivamente dá boot em nossa aplicação.

Criando uma nova App
--------------------

O objeto App recebe em seu construtor uma lista de conexões. As conexões são a forma de dizer ao asyncowker como falar com as origens dos estímulos. São esses estímulos que farão com que seus handler sejam executados.

As conexões possíveis estão mo módulo :py:mod:`asyncworker.connections`.

As instâncias dessas conexões podem ser usadas dentro do handlers, se necessário.


.. _asyncworker-app-handler:

Definindo handlers em sua App Asyncworker
-----------------------------------------

A forma de definir um novo handler em sua app Asyncworker depende do backend que você estiver usando. Cada backend (HTTP, AMQP, etc) expõe
uma interface para que esse registro seja feito.

Para mais detalhes veja a documentação específica do backend que você quer usar: :ref:`Tipos de Handlers <handler-types>`.
