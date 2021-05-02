from asyncworker.conf import settings
from asyncworker.metrics.buckets import exponential_buckets
from asyncworker.metrics.types import Histogram, Gauge

request_duration = Histogram(
    name="http_request_duration_ms",
    documentation="HTTP request duration in milliseconds",
    labelnames=("method", "path", "status"),
    buckets=settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS,
)

requests_in_progress = Gauge(
    name="http_requests_in_progress",
    documentation="Count of HTTP requests currently in progress",
    labelnames=("method", "path"),
)

response_size = Histogram(
    name="http_response_size_bytes",
    documentation="HTTP response size in bytes",
    labelnames=("method", "path"),
    buckets=exponential_buckets(start=100, factor=10, count=5),
)
