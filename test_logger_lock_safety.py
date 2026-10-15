"""Regression checks for logging paths that run in the scheduler process."""
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path


class LoggerLockSafetyTests(unittest.TestCase):
    def test_retention_cleanup_completes_with_stdout_intercepted(self):
        """Retention must not re-enter LOG_LOCK through DualLogStream.print()."""
        script = textwrap.dedent(
            """
            import io
            import sys
            import tempfile
            from datetime import datetime, timedelta
            from pathlib import Path

            import logger_setup

            with tempfile.TemporaryDirectory() as tmp:
                logger_setup.LOGS_DIR = Path(tmp)
                stale = logger_setup.LOGS_DIR / "running_2000-01-01.log"
                stale.write_text("old log", encoding="utf-8")
                sys.stdout = logger_setup.DualLogStream(io.StringIO())
                deleted = logger_setup.cleanup_old_logs(retention_days=3)
                assert deleted == [stale.name]
            """
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
