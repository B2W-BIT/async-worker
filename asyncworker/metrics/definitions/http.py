from asyncworker.conf import INFINITY
from asyncworker.metrics.types import Histogram

request_duration = Histogram(
    name="asyncworker_http_request_duration",
    documentation="HTTP request duration",
    labelnames=("method", "path", "status"),
    buckets=(0.01, 0.05, 0.1, INFINITY),
)
