import prometheus_client as prometheus

REGISTRY = prometheus.CollectorRegistry(auto_describe=True)
generate_latest = prometheus.generate_latest
