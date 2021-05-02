.. _asyncworker-auto-metrics:

Métricas expostas automaticamente
===================================


O asyncworker já expõe automaticamente algumas métricas. Porém algumas métricas são independentes do tipo de handler e elas estão documentadas aqui.


Nota sobre as métricas expostas automaticamente
-------------------------------------------------

Todas as métricas mostradas aqui também obedecem às :ref:`regras de formação de nome de métricas <metrics-config>`.


Métricas que são expostas por cada tipo de handler
-----------------------------------------------------

Cada tipo de handler expõe métricas específicas sobre seu domínio e mais detalhes sobre quais são essas métricas podem ser encontrados na documentação :ref:`dos tipos de handler <handler-types>` suportados pelo asyncworker.


Métricas que são independente do tipo de handler
---------------------------------------------------

Aqui listamos métricas que são relacionadas ao processo Python.


Métricas sobre versão do Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Uma métrica é exposta contendo a versão do python que o código está rodando. O nome dessa métrica é ``python_info``. Essa métrica possui as seguintes labels:

 - ``version``
 - ``implementation``
 - ``major``
 - ``minor``
 - ``patchlevel``

Todas essas informações são extraídas do módulo ``platform`` da `stdlib <https://docs.python.org/3/library/platform.html>`_.

Métricas sobre o processo Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Algumas métricas sobre o processo do Python também são expostas por padrão. São elas:


 - ``process_virtual_memory_bytes``
 - ``process_resident_memory_bytes``
 - ``process_start_time_seconds``
 - ``process_cpu_seconds_total``
 - ``process_open_fds``
 - ``process_max_fds``



Métricas sobre o Garbage Collector do Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Essas são métricas sobre o Garbage Collector. Todos os dados são extraídos do módulo ``gc`` da `stdlib <https://docs.python.org/3/library/gc.html>`_.


- ``python_gc_objects_collected_total``
- ``python_gc_objects_uncollectable_total``
- ``python_gc_collections_total``

Cada uma dessas métricas possui uma label, ``generation``. Os valores dessa label vêm também diretamente do módulo ``gc``.
