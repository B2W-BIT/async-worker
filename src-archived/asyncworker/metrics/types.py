from abc import ABCMeta

import prometheus_client as prometheus

from asyncworker.conf import settings
from asyncworker.metrics.registry import REGISTRY, NAMESPACE


class Metric(metaclass=ABCMeta):
    pass


class Counter(Metric, prometheus.Counter):
    def __init__(self, name: str, documentation: str, **kwargs) -> None:
        kwargs["namespace"] = NAMESPACE
        kwargs["registry"] = REGISTRY
        super().__init__(name, documentation, **kwargs)


class Histogram(Metric, prometheus.Histogram):
    def __init__(self, name: str, documentation: str, **kwargs) -> None:
        kwargs["namespace"] = NAMESPACE
        kwargs["registry"] = REGISTRY
        if not kwargs.get("buckets"):
            kwargs["buckets"] = settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS
        super().__init__(name, documentation, **kwargs)


class Gauge(Metric, prometheus.Gauge):
    def __init__(self, name: str, documentation: str, **kwargs) -> None:
        kwargs["namespace"] = NAMESPACE
        kwargs["registry"] = REGISTRY
        super().__init__(name, documentation, **kwargs)
