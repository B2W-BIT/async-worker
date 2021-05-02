import gc
import platform

from prometheus_client import CollectorRegistry
from prometheus_client.metrics_core import CounterMetricFamily

from asyncworker.metrics.collectors.base import BaseCollector


class GCCollector(BaseCollector):
    """
    Collector for Garbage collection statistics.
    Esse código veio do prometheus_client (https://github.com/prometheus/client_python/blob/6b091aba77db44459290808368bd4ab913ef8ba5/prometheus_client/gc_collector.py)
    Foi modificado para que possamos ter um namespace em suas métricas

    """

    def __init__(
        self, registry: CollectorRegistry, namespace: str = "", gc=gc
    ) -> None:
        if (
            not hasattr(gc, "get_stats")
            or platform.python_implementation() != "CPython"
        ):
            return
        if namespace:
            self.namespace = f"{namespace}_"
        registry.register(self)

    def collect(self):
        collected = CounterMetricFamily(
            f"{self.namespace}python_gc_objects_collected",
            "Objects collected during gc",
            labels=["generation"],
        )
        uncollectable = CounterMetricFamily(
            f"{self.namespace}python_gc_objects_uncollectable",
            "Uncollectable object found during GC",
            labels=["generation"],
        )

        collections = CounterMetricFamily(
            f"{self.namespace}python_gc_collections",
            "Number of times this generation was collected",
            labels=["generation"],
        )

        for generation, stat in enumerate(gc.get_stats()):
            generation = str(generation)
            collected.add_metric([generation], value=stat["collected"])
            uncollectable.add_metric([generation], value=stat["uncollectable"])
            collections.add_metric([generation], value=stat["collections"])

        return [collected, uncollectable, collections]
