Compatibilidade de Versões do asyncowker
========================================

O versionamento do projeto segue a mesma linha do `Semver <https://semver.org/>`_ mas com uma peculiaridade. Como esse é um projeto que ainda está em pleno desenvolvimento ainda falta um longo caminho até chegarmos a uma versão ``1.0``.

Por isso que fazemos é o seguinte: Mudamos apenas os valores da ``MINOR`` e ``PATCH``.

Quando mudamos apenas a ``PATCH`` version significa que o código novo é retro-compatível com o antigo, ou seja, pode ser atualizado sem problemas. Sem precisar olhar changelogs.

Quando mudamos a ``MINOR`` version significa que o changelog requer atenção. Seja um mudança simples ou uma mudança mais complexa que vai demandar ajuster no seu código é recomendado que você olhe o changelog da nova versão para saber se você precisa ajustar alguma coisa.

Lembrando que a formação da versão é ``0.MINOR.PATCH``.


Atualização de dependências
---------------------------

O asyncworker depende basicamente de dois outros projetos: `aiohttp <https://docs.aiohttp.org/en/stable/>`_ e `Pydantic <https://pydantic-docs.helpmanual.io/>`_.

Sempre que quaisquer dessas duas dependências precisarem ser atualizadas isso será considerado uma mudança (potencialmente) retro-incompatível e por isso o asyncworker terá sua minor version aumentada.
