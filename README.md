# LogLens

A Python log-analysis tool for investigating application errors.

## Progress
- Built a local command-line log summarizer.
- Added service filtering and malformed-line reporting.
- Verified the parser and summarizer with four passing tests.

## Run the local prototype

Requires Python 3.11 or newer. No third-party packages are needed.
The Python source, tests, and sample data are currently saved locally and have not yet been uploaded to this repository. These commands apply to that local project folder.

```sh
python3 -m loglens summarize data/sample.log
python3 -m loglens summarize data/sample.log --service api
python3 -m unittest discover -s tests -v
```

The sample contains 10 valid entries: 5 INFO, 1 WARNING, 3 ERROR, and 1 CRITICAL. One malformed line is reported separately.

## Next step

Synchronize the local Python source, sample logs, and tests with this repository.
## Log format
Each nonblank line uses four fields separated by ` | ` (a space, a pipe, and a space):
```text
2026-10-23T09:00:00 | ERROR | api | Database timeout
```
- Timestamp: a value accepted by Python's `datetime.fromisoformat`.
- Severity: exactly `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` (uppercase).
- Service: a nonempty service name, such as `api` or `worker`.
- Message: a nonempty description; additional ` | ` separators stay in the message.
Blank lines are ignored. Lines with missing fields, invalid timestamps, unknown severities, or empty services/messages are counted as malformed. The malformed count covers the entire file, even when filtering by service. Service matching is exact and case-sensitive.
The frequent-error list groups identical message text across selected services and includes both ERROR and CRITICAL entries, showing up to five messages. This prototype supports the format above; it does not yet parse arbitrary application logs.
