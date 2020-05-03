from abc import ABCMeta

import prometheus_client as prometheus

from asyncworker.conf import settings


class _BaseMetric(metaclass=ABCMeta):
    pass


class Counter(_BaseMetric, prometheus.Counter):
    pass


class Histogram(_BaseMetric, prometheus.Histogram):
    DEFAULT_BUCKETS = settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS


class Gauge(_BaseMetric, prometheus.Gauge):
    pass
