from asyncworker.conf import settings
from .types import Counter, Histogram, Gauge


active_consumers = Gauge(
    name="asyncworker_amqp_active_consumers",
    documentation="Count of active consumers",
)

processed_messages = Counter(
    name="asyncworker_amqp_processed_messages",
    documentation="Count of total processed messages",
    labelnames=("queue_name", "action"),
)

active_connections = Gauge(
    name="asyncworker_amqp_active_connections",
    documentation="Count of active AMQP connections",
)

filled_buckets = Counter(
    name="asyncworker_amqp_filled_buckets",
    documentation="Count of total AMQP filled buckets",
)

flushed_buckets = Counter(
    name="asyncworker_amqp_flushed_buckets",
    documentation="Count of total AMQP buckets flushed due to ",
)

bucket_handle_duration = Histogram(
    name="asyncworker_amqp_bucket_handle",
    documentation="Duration of message handling",
    buckets=settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS,
)
