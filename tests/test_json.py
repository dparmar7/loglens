"""Verify the machine-readable CLI contract."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class JsonOutputTests(unittest.TestCase):
    def run_json(self, contents, *options):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.log"
            path.write_text(contents, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "loglens", "summarize", str(path),
                 "--json", *options],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True, text=True, timeout=10,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def test_filtered_summary_preserves_messages_and_malformed_count(self):
        report = self.run_json(
            '2026-10-29 | ERROR | api | Timeout "retry"\\connection\n'
            '2026-10-29 | ERROR | api | Timeout "retry"\\connection\n'
            '2026-10-29 | CRITICAL | worker | Worker stopped\n'
            'broken\n', "--service", "api",
        )
        self.assertEqual(report, {
            "total": 2,
            "severities": {"DEBUG": 0, "INFO": 0, "WARNING": 0,
                           "ERROR": 2, "CRITICAL": 0},
            "malformed": 1,
            "top_errors": [{"message": 'Timeout "retry"\\connection', "count": 2}],
        })

    def test_empty_input_has_stable_fields(self):
        report = self.run_json("")
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["malformed"], 0)
        self.assertEqual(report["top_errors"], [])
        self.assertEqual(len(report["severities"]), 5)
        self.assertTrue(all(value == 0 for value in report["severities"].values()))


if __name__ == "__main__":
    unittest.main()
