"""Dependency-free regression checks for web scheduler lifecycle wiring."""
import ast
import unittest
from pathlib import Path


class SchedulerLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = Path(__file__).with_name("web_server.py").read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    def test_startup_retains_a_scheduler_supervisor_task(self):
        self.assertIn("_scheduler_supervisor_task", self.source)
        self.assertIn("scheduler_supervisor_loop", self.source)
        self.assertIn("name=\"daily-work-scheduler-supervisor\"", self.source)

    def test_watchdog_restarts_stale_linux_scheduler_through_systemd(self):
        self.assertIn("_SCHEDULER_WATCHDOG_TIMEOUT_SECONDS = 300", self.source)
        self.assertIn("os._exit(75)", self.source)
        self.assertIn("_touch_scheduler_heartbeat()", self.source)

    def test_shutdown_cancels_the_retained_scheduler_task(self):
        self.assertIn("async def stop_scheduler_task", self.source)
        self.assertIn("task.cancel()", self.source)


if __name__ == "__main__":
    unittest.main()
