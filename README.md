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
