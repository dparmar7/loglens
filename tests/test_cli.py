"""Exercise the public CLI in a separate Python process."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "-m", "loglens", *map(str, arguments)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_service_filter_excludes_other_services(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.log"
            path.write_text(
                "2026-10-27T09:00:00 | ERROR | api | API timeout\n"
                "2026-10-27T09:00:01 | CRITICAL | worker | Worker stopped\n"
                "malformed entry\n",
                encoding="utf-8",
            )
            result = self.run_cli("summarize", path, "--service", "api")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("Total entries: 1", result.stdout.splitlines())
        self.assertIn("ERROR: 1", result.stdout.splitlines())
        self.assertIn("CRITICAL: 0", result.stdout.splitlines())
        self.assertIn("Malformed lines (whole file): 1", result.stdout)
        self.assertIn("1 x API timeout", result.stdout)
        self.assertNotIn("Worker stopped", result.stdout)

    def test_missing_file_reports_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.log"
            result = self.run_cli("summarize", path)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("Could not read log file:", result.stderr)
        self.assertIn("missing.log", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_file_argument_shows_usage(self):
        result = self.run_cli("summarize")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("usage:", result.stderr)
        self.assertIn("file", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
