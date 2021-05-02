from prometheus_client import CollectorRegistry

from asyncworker.conf import settings
from asyncworker.metrics.collectors.gc import GCCollector
from asyncworker.metrics.collectors.platform import PlatformCollector
from asyncworker.metrics.collectors.process import ProcessCollector

NAMESPACE = (
    f"{settings.METRICS_NAMESPACE}_{settings.METRICS_APPPREFIX}"
    if settings.METRICS_APPPREFIX
    else f"{settings.METRICS_NAMESPACE}"
)


REGISTRY = CollectorRegistry(auto_describe=True)

PLATFORM_COLLECTOR = PlatformCollector(registry=REGISTRY, namespace=NAMESPACE)
PROCESS_COLLECTOR = ProcessCollector(namespace=NAMESPACE, registry=REGISTRY)
GC_COLLECTOR = GCCollector(registry=REGISTRY, namespace=NAMESPACE)
