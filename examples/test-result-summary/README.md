# Test Result Summary

A small portfolio example showing how to turn test execution data into a readable summary. All data is fictional. This is demonstration code, not an enterprise framework or a production reporting system.

## What it does

Reads a CSV containing `test_id` and `status`, checks each row, and prints counts and a pass rate as JSON. Supported statuses are `passed`, `failed`, and `skipped` (case-insensitive). The pass rate uses **all** rows, including skipped tests; an empty input has a `null` rate. It does not deduplicate test IDs or interpret retries.

## Run

Requires Python 3.8 or newer; no third-party packages. From this folder:

```bash
python3 summary.py results.csv
python3 -m unittest -v
```

Expected sample output:

```json
{
  "total": 4,
  "passed": 2,
  "failed": 1,
  "skipped": 1,
  "pass_rate_percent": 50.0
}
```

An invalid row or missing required column produces an error and a nonzero exit code. To adapt it, export a CSV with the same column names and supported status values; do not put sensitive test data in a public repository.

## Next steps

For real delivery pipelines, agree on how retries, skipped tests and duplicate executions are counted, then add a supported report format and build-level metadata before using the result for release decisions.
