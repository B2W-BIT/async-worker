from abc import ABCMeta

import prometheus_client as prometheus


class _BaseMetric(metaclass=ABCMeta):
    pass


class Counter(_BaseMetric, prometheus.Counter):
    pass


class Histogram(_BaseMetric, prometheus.Histogram):
    pass


class Gauge(_BaseMetric, prometheus.Gauge):
    pass
