# LogLens

A Python command-line tool for summarizing application logs and investigating recurring errors.

LogLens converts structured log entries into severity counts and frequent-error summaries. The project is being developed toward a searchable incident investigation platform with an evaluated machine learning component.

## Project status

**Early development.** The repository includes a working command-line prototype, synthetic sample logs, and nine passing tests.

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

Clone the repository and enter the project directory:

```sh
git clone https://github.com/dparmar7/loglens.git
cd loglens
```

Run the following commands from this directory.

Summarize a log file:

```sh
python3 -m loglens summarize data/sample.log
```

Filter by service:

```sh
python3 -m loglens summarize data/sample.log --service api
```

### JSON output

Export a summary that other programs can read:

```sh
python3 -m loglens summarize data/sample.log --json
```

Combine `--json` with `--service api` to export only that service. Successful JSON output contains `total`, `severities` (all five levels, including zeros), `malformed` (whole-file count), and `top_errors` (up to five objects with `message` and `count`). Empty input produces zero counts and an empty error list. File errors still appear on stderr with a nonzero exit code.

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

The nine tests cover parsing, message separators, invalid fields, service filtering and counts, blank lines, empty files, and command-line behavior. CLI tests run LogLens in a separate Python process to verify output, exit codes, and clear error messages for missing files and required arguments. JSON tests verify service filtering, malformed-line counts, empty input, and preservation of quoted messages.

## Roadmap

1. Expand log querying and storage.
2. Introduce SQLite storage and queries by service and time.
3. Build a REST API and an investigation interface.
4. Evaluate anomaly detection against a simple baseline using held-out data.
5. Add container packaging and a deployed demonstration.

## Limitations

The prototype supports the documented log format only. It does not currently provide arbitrary log-format detection, persistent storage, real-time monitoring, or machine learning predictions.
