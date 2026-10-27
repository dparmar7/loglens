import tempfile
import unittest
from pathlib import Path

from loglens.__main__ import parse_line, summarize


class SummaryTests(unittest.TestCase):
    def test_parser_preserves_message_separator(self):
        entry = parse_line("2026-10-20T09:00:00 | INFO | api | first | second")
        self.assertEqual(entry["message"], "first | second")

    def test_rejects_invalid_fields(self):
        for line in ("broken", "bad-date | INFO | api | hello",
                     "2026-10-20 | UNKNOWN | api | hello",
                     "2026-10-20 | INFO |  | hello"):
            with self.subTest(line=line), self.assertRaises(ValueError):
                parse_line(line)

    def test_counts_filters_and_skips_blank_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.log"
            path.write_text("2026-10-20 | ERROR | api | timeout\n"
                            "2026-10-20 | CRITICAL | worker | stopped\n"
                            "broken\n\n", encoding="utf-8")
            result = summarize(path, service="api")
            self.assertEqual(result["total"], 1)
            self.assertEqual(result["errors"]["timeout"], 1)
            self.assertEqual(result["malformed"], 1)
            self.assertEqual(summarize(path)["total"], 2)

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.log"
            path.touch()
            self.assertEqual(summarize(path)["total"], 0)


if __name__ == "__main__":
    unittest.main()
