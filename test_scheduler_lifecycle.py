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

    def test_retention_cleanup_cannot_block_due_slot_evaluation(self):
        scheduler_start = self.source.index("async def background_scheduler_loop")
        scheduler_source = self.source[scheduler_start:]
        self.assertIn("async def _run_scheduled_retention_cleanup", self.source)
        self.assertIn("name=\"daily-work-scheduler-maintenance\"", scheduler_source)
        self.assertNotIn("await asyncio.to_thread(cleanup_retained_files)", scheduler_source)
        self.assertLess(
            scheduler_source.index("schedule_slots = db_manager.get_schedule_times()"),
            scheduler_source.index("maintenance_task = asyncio.create_task("),
        )

    def test_due_slot_tasks_are_retained_until_completion(self):
        self.assertIn("scheduled_slot_tasks: Dict[int, asyncio.Task] = {}", self.source)
        self.assertIn("scheduled_slot_tasks[slot_id] = slot_task", self.source)
        self.assertIn("slot_task.add_done_callback", self.source)


if __name__ == "__main__":
    unittest.main()
