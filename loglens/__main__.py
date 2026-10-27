"""Command-line entry point: python -m loglens summarize FILE."""

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path


def parse_line(line):
    """Parse timestamp | severity | service | message, or raise ValueError."""
    parts = line.strip().split(" | ", 3)
    if len(parts) != 4:
        raise ValueError("expected four fields separated by ' | '")
    timestamp, severity, service, message = parts
    datetime.fromisoformat(timestamp)
    if severity not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ValueError("unknown severity")
    if not service.strip() or not message.strip():
        raise ValueError("service and message must not be empty")
    return {"timestamp": timestamp, "severity": severity,
            "service": service, "message": message}


def summarize(path, service=None):
    """Read one line at a time and count valid, selected entries."""
    severities = Counter()
    errors = Counter()
    malformed = 0
    with path.open(encoding="utf-8") as log_file:
        for line in log_file:
            if not line.strip():
                continue
            try:
                entry = parse_line(line)
            except ValueError:
                malformed += 1
                continue
            if service is not None and entry["service"] != service:
                continue
            severities[entry["severity"]] += 1
            if entry["severity"] in {"ERROR", "CRITICAL"}:
                errors[entry["message"]] += 1
    return {"total": sum(severities.values()), "severities": severities,
            "errors": errors, "malformed": malformed}


def main():
    parser = argparse.ArgumentParser(description="Summarize application logs")
    commands = parser.add_subparsers(dest="command", required=True)
    summary = commands.add_parser("summarize", help="Count entries and errors")
    summary.add_argument("file", type=Path)
    summary.add_argument("--service", help="Only count this service")
    args = parser.parse_args()
    try:
        result = summarize(args.file, args.service)
    except (OSError, UnicodeError) as error:
        parser.exit(1, f"Could not read log file: {error}\n")
    print(f"Total entries: {result['total']}")
    for severity in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        print(f"{severity}: {result['severities'][severity]}")
    print(f"Malformed lines (whole file): {result['malformed']}")
    print("Most frequent errors:")
    for message, count in result["errors"].most_common(5):
        print(f"  {count} x {message}")
    if not result["errors"]:
        print("  None")


if __name__ == "__main__":
    main()
