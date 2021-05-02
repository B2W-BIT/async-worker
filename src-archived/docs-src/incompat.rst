.. _incompat:

Incompatibilidades
==================

.. toctree::
   :maxdepth: 2
   :titlesonly:

Atualmente, pelo fato o asyncworker usar o `aiologger <https://github.com/b2wdigital/aiologger>`_, ele é incompatível com apps que usam **múltiplos** loops de evento. Ou seja, se sua app cria um novo loop e substitui o loop anterior isso causará um problema com os logs gerados pelo asyncworker (via aiologger).

No geral, as aplicações assíncronas usam apenas um loop de evento durante todo o seu ciclo de vida. Isso significa que a não se que você esteja escrevendo um código com um comportamento muito específico (que dependa da renovação do loop de eventos) você não terá maiores problemas em usar o asyncworker.

Essa incompatibilidade do aiologger está sendo tratada na issue `#35 <https://github.com/b2wdigital/aiologger/issues/35>`_.
O projeto tem como objetivo ser um framework para escrever workers assíncronos em python. Por worker entende-se qualquer aplicação que rode por tempo indeterminado e que receba estímulos de várias origens diferentes. Essas orignes podem ser:
