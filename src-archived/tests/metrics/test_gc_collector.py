import os
from importlib import reload

from asynctest import TestCase, mock


class GCCollectorest(TestCase):
    async def test_use_global_namespace(self):
        from asyncworker import conf
        from asyncworker.metrics import registry

        with mock.patch.dict(os.environ, ASYNCWORKER_METRICS_APPPREFIX="myapp"):
            reload(conf)
            reload(registry)
            pc = registry.GC_COLLECTOR

            metrics = pc.collect()
            self.assertEqual(3, len(pc.collect()))

            metric_names = [m.name for m in metrics]
            expexted_metric_names = [
                "asyncworker_myapp_python_gc_objects_collected",
                "asyncworker_myapp_python_gc_objects_uncollectable",
                "asyncworker_myapp_python_gc_collections",
            ]
            self.assertEqual(expexted_metric_names, metric_names)

            expected_samples_names_collected = [
                "asyncworker_myapp_python_gc_objects_collected_total",
                "asyncworker_myapp_python_gc_objects_collected_total",
                "asyncworker_myapp_python_gc_objects_collected_total",
            ]
            samples_names_collected = [s.name for s in metrics[0].samples]
            self.assertEqual(
                expected_samples_names_collected, samples_names_collected
            )

            expected_samples_names_uncollectable = [
                "asyncworker_myapp_python_gc_objects_uncollectable_total",
                "asyncworker_myapp_python_gc_objects_uncollectable_total",
                "asyncworker_myapp_python_gc_objects_uncollectable_total",
            ]
            samples_names_uncollectable = [s.name for s in metrics[1].samples]
            self.assertEqual(
                expected_samples_names_uncollectable,
                samples_names_uncollectable,
            )

            expected_samples_names_collections = [
                "asyncworker_myapp_python_gc_collections_total",
                "asyncworker_myapp_python_gc_collections_total",
                "asyncworker_myapp_python_gc_collections_total",
            ]
            samples_names_collections = [s.name for s in metrics[2].samples]
            self.assertEqual(
                expected_samples_names_collections, samples_names_collections
            )

    async def test_do_nothing_if_gc_does_not_have_get_stats(self):
        from asyncworker.metrics.collectors import gc as gc_collector

        registry_mock = mock.MagicMock()
        gc_mock = mock.MagicMock()
        del gc_mock.get_stats

        gc_collector.GCCollector(registry=registry_mock, gc=gc_mock)
        self.assertEqual(0, registry_mock.register.call_count)

    async def test_do_nothing_if_is_not_cpython(self):
        from asyncworker.metrics.collectors import gc as gc_collector

        registry_mock = mock.MagicMock()
        with mock.patch("platform.python_implementation") as gc_mock:
            gc_mock.return_value = "Jython"
            gc_collector.GCCollector(registry=registry_mock)
            self.assertEqual(0, registry_mock.register.call_count)
