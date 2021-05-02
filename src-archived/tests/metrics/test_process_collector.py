import os
from importlib import reload

from asynctest import TestCase, mock


class ProcessCollectorTest(TestCase):
    async def test_use_global_namespace(self):
        from asyncworker import conf
        from asyncworker.metrics import registry

        with mock.patch.dict(os.environ, ASYNCWORKER_METRICS_APPPREFIX="myapp"):
            reload(conf)
            reload(registry)
            pc = registry.PROCESS_COLLECTOR

            metrics = pc.collect()
            self.assertEqual(6, len(pc.collect()))

            metric_names = [m.name for m in metrics]
            expexted_metric_names = [
                "asyncworker_myapp_process_virtual_memory_bytes",
                "asyncworker_myapp_process_resident_memory_bytes",
                "asyncworker_myapp_process_start_time_seconds",
                "asyncworker_myapp_process_cpu_seconds",
                "asyncworker_myapp_process_open_fds",
                "asyncworker_myapp_process_max_fds",
            ]
            self.assertEqual(expexted_metric_names, metric_names)
