import platform as pf

from prometheus_client.metrics_core import GaugeMetricFamily


class PlatformCollector(object):
    """
    Collector for python platform information

    Esse código veio do prometheus_client (https://github.com/prometheus/client_python/blob/6b091aba77db44459290808368bd4ab913ef8ba5/prometheus_client/platform_collector.py)
    Foi modificado para que possamos ter um namespace em suas métricas
    """

    def __init__(self, registry, namespace=""):
        self._platform = pf
        info = self._info()

        if namespace:
            self.namespace = f"{namespace}_"

        self._metrics = [
            self._add_metric(
                f"{self.namespace}python_info",
                "Python platform information",
                info,
            )
        ]

        registry.register(self)

    def collect(self):
        return self._metrics

    @staticmethod
    def _add_metric(name, documentation, data):
        labels = data.keys()
        values = [data[k] for k in labels]
        g = GaugeMetricFamily(name, documentation, labels=labels)
        g.add_metric(values, 1)
        return g

    def _info(self):
        major, minor, patchlevel = self._platform.python_version_tuple()
        return {
            "version": self._platform.python_version(),
            "implementation": self._platform.python_implementation(),
            "major": major,
            "minor": minor,
            "patchlevel": patchlevel,
        }
