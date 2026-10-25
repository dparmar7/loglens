# LogLens

A Python command-line tool for summarizing application logs and investigating recurring errors.

LogLens converts structured log entries into severity counts and frequent-error summaries. The project is being developed toward a searchable incident investigation platform with an evaluated machine learning component.

## Project status

**Early development.** The command-line prototype, sample data, and four unit tests are implemented locally. This repository currently contains documentation; the source files have not yet been published.

Database storage, an API, a web interface, and anomaly detection are planned features.

## Current capabilities

- Parse structured log files one line at a time.
- Count valid entries by severity.
- Filter entries by service name.
- Display up to five of the most frequent error messages.
- Report malformed lines separately from valid entries.

## Requirements

- Python 3.11 or newer
- No third-party Python packages

## Usage

Run the following commands from the local project directory containing the `loglens/`, `data/`, and `tests/` folders. These commands require the local source files and will not work from a clone of this documentation-only repository yet.

Summarize a log file:

```sh
python3 -m loglens summarize data/sample.log
```

Filter by service:

```sh
python3 -m loglens summarize data/sample.log --service api
```

### Example output

The local sample file produces:

```text
Total entries: 10
DEBUG: 0
INFO: 5
WARNING: 1
ERROR: 3
CRITICAL: 1
Malformed lines (whole file): 1
Most frequent errors:
  2 x Database timeout
  1 x Job failed
  1 x Database unavailable
```

## Log format

Each nonblank line contains four fields separated by a space, a pipe, and a space (` | `):

```text
2026-10-24T09:00:00 | ERROR | api | Database timeout
```

| Field | Accepted value |
| --- | --- |
| Timestamp | A value accepted by Python's `datetime.fromisoformat` |
| Severity | `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` |
| Service | A nonempty service name |
| Message | A nonempty description |

### Parsing behavior

- Blank lines are ignored.
- Missing fields, invalid timestamps, unsupported severities, and empty services or messages are counted as malformed.
- The malformed-line count covers the entire file, including when a service filter is active.
- Severity values must be uppercase. Service matching is exact and case-sensitive.
- Additional ` | ` separators are preserved within the message.
- Frequent-error summaries include both `ERROR` and `CRITICAL` entries and group identical message text across the selected services.

## Testing

Run the local test suite:

```sh
python3 -m unittest discover -s tests -v
```

The four existing tests cover message separators, invalid fields, service filtering and counts, blank lines, and empty files.

## Roadmap

1. Publish the local source code, sample logs, and tests.
2. Add structured JSON output and command-line failure tests.
3. Introduce SQLite storage and queries by service and time.
4. Build a REST API and an investigation interface.
5. Evaluate anomaly detection against a simple baseline using held-out data.
6. Add automated checks, container packaging, and a deployed demonstration.

## Limitations

The prototype supports the documented log format only. It does not currently provide arbitrary log-format detection, persistent storage, real-time monitoring, or machine learning predictions.
