from http import HTTPStatus
from importlib import reload

from aiohttp import web
from asynctest import mock, TestCase
from prometheus_client import CollectorRegistry, generate_latest
from prometheus_client.parser import text_string_to_metric_families

from asyncworker import App, RouteTypes
from asyncworker.conf import settings
from asyncworker.http.decorators import parse_path
from asyncworker.metrics import Counter, Gauge, Histogram
from asyncworker.metrics.aiohttp_resources import metrics_route_handler
from asyncworker.metrics.registry import REGISTRY, NAMESPACE
from asyncworker.testing import HttpClientContext


class MetricsEndpointTest(TestCase):
    use_default_loop = True
    maxDiff = None

    async def setUp(self):
        self.METRICS_PATH = "/metrics-2"
        self.app = App()
        self.app.http.get([self.METRICS_PATH])(metrics_route_handler)

    async def test_metrics_namespace(self):
        def _check_metrics_cant_override_namespace(metric, metric_name):
            result = metric.collect()
            self.assertEqual(1, len(result))
            self.assertEqual(f"{NAMESPACE}_{metric_name}", result[0].name)

        namespace = "namespaace"
        _check_metrics_cant_override_namespace(
            Counter("counter_with_namespace", "Doc", namespace=namespace),
            "counter_with_namespace",
        )
        _check_metrics_cant_override_namespace(
            Gauge("gauge_with_ns", "doc", namespace=namespace), "gauge_with_ns"
        )
        _check_metrics_cant_override_namespace(
            Histogram("histogram_with_ns", "doc", namespace=namespace),
            "histogram_with_ns",
        )

    async def test_histogram_override_buckets(self):
        h = Histogram(
            "my_new_histogram", "New Histogram", buckets=[7.0, 12.0, 30.0]
        )
        h.observe(5)
        h.observe(9)

        samples = h.collect()[0].samples
        self.assertEqual(
            {"value": 1.0, "le": "7.0"},
            {"value": samples[0].value, **samples[0].labels},
        )
        self.assertEqual(
            {"value": 2.0, "le": "12.0"},
            {"value": samples[1].value, **samples[1].labels},
        )
        self.assertEqual(
            {"value": 2.0, "le": "30.0"},
            {"value": samples[2].value, **samples[2].labels},
        )

    async def test_metric_cant_override_registry(self):
        registry = CollectorRegistry()
        Counter("counter", "Doc", registry=registry)
        Gauge("gauge", "Doc", registry=registry)
        Histogram("histogram", "Doc", registry=registry)
        self.assertEqual(b"", generate_latest(registry))

    async def test_metrics_with_app_prefix(self):
        import os
        from asyncworker.metrics import types, registry
        from asyncworker import conf

        with mock.patch.dict(os.environ, ASYNCWORKER_METRICS_APPPREFIX="myapp"):
            reload(conf)
            reload(registry)
            reload(types)
            self.assertEqual("myapp", conf.settings.METRICS_APPPREFIX)
            c = types.Counter("my_other_counter", "Docs")
            result = c.collect()[0]
            self.assertEqual("asyncworker_myapp_my_other_counter", result.name)

            g = Gauge("my_other_gauge", "Docs")
            self.assertEqual(
                "asyncworker_myapp_my_other_gauge", g.collect()[0].name
            )

            h = Histogram("my_other_histogram", "docs")
            self.assertEqual(
                "asyncworker_myapp_my_other_histogram", h.collect()[0].name
            )

    async def test_count_metric(self):
        metric_name = "myapp_example_counter"
        counter = Counter(metric_name, "Um contador simples")

        @self.app.http.get(["/foo"])
        async def _handler():
            counter.inc()
            return web.json_response({})

        async with HttpClientContext(self.app) as client:
            await client.get("/foo")
            await client.get("/foo")

            metrics = await client.get(self.METRICS_PATH)
            self.assertEqual(HTTPStatus.OK, metrics.status)

            data = await metrics.text()
            metrics_parsed = list(text_string_to_metric_families(data))
            count_metric = [
                m
                for m in metrics_parsed
                if m.name == f"{NAMESPACE}_{metric_name}"
            ]
            self.assertEqual(1, len(count_metric))
            self.assertEqual(2.0, count_metric[0].samples[0].value)

    async def test_gauge_metric(self):
        metric_name = "myapp_example_gauge"
        gauge = Gauge(metric_name, "um Gauge simples", registry=REGISTRY)

        @self.app.http.get(["/foo/{value}"])
        @parse_path
        async def _handler(value: int):
            gauge.inc(value)
            return web.json_response({})

        async with HttpClientContext(self.app) as client:
            await client.get("/foo/10")
            await client.get("/foo/20")
            await client.get("/foo/-5")

            metrics = await client.get(self.METRICS_PATH)
            self.assertEqual(HTTPStatus.OK, metrics.status)

            data = await metrics.text()
            metrics_parsed = list(text_string_to_metric_families(data))
            gauge_metric = [
                m
                for m in metrics_parsed
                if m.name == f"{NAMESPACE}_{metric_name}"
            ]
            self.assertEqual(1, len(gauge_metric))
            self.assertEqual(25.0, gauge_metric[0].samples[0].value)

    async def test_histogram_metric(self):
        metric_name = "myapp_example_histogram"
        histogram = Histogram(
            metric_name, "um Histogram simples", registry=REGISTRY
        )

        @self.app.http.get(["/foo/{value}"])
        @parse_path
        async def _handler(value: int):
            histogram.observe(value)
            return web.json_response({})

        async with HttpClientContext(self.app) as client:
            await client.get("/foo/8")
            await client.get("/foo/20")
            await client.get("/foo/12")
            await client.get("/foo/201")

            metrics = await client.get(self.METRICS_PATH)
            self.assertEqual(HTTPStatus.OK, metrics.status)

            data = await metrics.text()
            metrics_parsed = list(text_string_to_metric_families(data))
            histogram_metric = [
                m
                for m in metrics_parsed
                if m.name == f"{NAMESPACE}_{metric_name}"
            ]
            self.assertEqual(1, len(histogram_metric))
            self._assert_bucket_value(
                1.0,
                settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS[0],
                histogram_metric[0].samples[0],
            )
            self._assert_bucket_value(
                3.0,
                settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS[1],
                histogram_metric[0].samples[1],
            )
            self._assert_bucket_value(
                3.0,
                settings.METRICS_DEFAULT_HISTOGRAM_BUCKETS_IN_MS[3],
                histogram_metric[0].samples[3],
            )

    async def test_gc_collector_metric(self):

        async with HttpClientContext(self.app) as client:
            metrics = await client.get(self.METRICS_PATH)
            self.assertEqual(HTTPStatus.OK, metrics.status)

            data = await metrics.text()
            metrics_parsed = list(text_string_to_metric_families(data))
            python_gc_metrics = [
                m
                for m in metrics_parsed
                if m.name.startswith(f"{NAMESPACE}_python_gc")
            ]
            self.assertEqual(3, len(python_gc_metrics))
            python_gc_metric_names = [m.name for m in python_gc_metrics]
            self.assertEqual(
                [
                    "asyncworker_python_gc_objects_collected",
                    "asyncworker_python_gc_objects_uncollectable",
                    "asyncworker_python_gc_collections",
                ],
                python_gc_metric_names,
            )

    async def test_process_collector_metric(self):

        async with HttpClientContext(self.app) as client:
            metrics = await client.get(self.METRICS_PATH)
            self.assertEqual(HTTPStatus.OK, metrics.status)

            data = await metrics.text()
            metrics_parsed = list(text_string_to_metric_families(data))
            metrics = [
                m
                for m in metrics_parsed
                if m.name.startswith(f"{NAMESPACE}_process")
            ]
            self.assertEqual(6, len(metrics))
            metric_names = [m.name for m in metrics]
            self.assertEqual(
                [
                    "asyncworker_process_virtual_memory_bytes",
                    "asyncworker_process_resident_memory_bytes",
                    "asyncworker_process_start_time_seconds",
                    "asyncworker_process_cpu_seconds",
                    "asyncworker_process_open_fds",
                    "asyncworker_process_max_fds",
                ],
                metric_names,
            )

    async def test_platform_collector_metric(self):

        async with HttpClientContext(self.app) as client:
            metrics = await client.get(self.METRICS_PATH)
            self.assertEqual(HTTPStatus.OK, metrics.status)

            data = await metrics.text()
            metrics_parsed = list(text_string_to_metric_families(data))
            metrics = [
                m
                for m in metrics_parsed
                if m.name == f"{NAMESPACE}_python_info"
            ]
            self.assertEqual(1, len(metrics))
            metric_names = [m.name for m in metrics]
            self.assertEqual(["asyncworker_python_info"], metric_names)

    def _assert_bucket_value(self, expected_value, bucket_value, metric):
        self.assertEqual(
            {"value": expected_value, "le": str(float(bucket_value))},
            {"value": metric.value, **metric.labels},
        )
