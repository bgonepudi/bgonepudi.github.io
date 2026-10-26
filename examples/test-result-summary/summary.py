"""Summarize synthetic test results from a CSV file."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

VALID = {'passed', 'failed', 'skipped'}

def summarize(path):
    counts = Counter({status: 0 for status in sorted(VALID)})
    with Path(path).open(newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not {'test_id', 'status'}.issubset(reader.fieldnames):
            raise ValueError('CSV must contain test_id and status columns')
        for line, row in enumerate(reader, start=2):
            test_id = (row.get('test_id') or '').strip()
            status = (row.get('status') or '').strip().lower()
            if not test_id or status not in VALID:
                raise ValueError(f'Invalid test_id or status on line {line}')
            counts[status] += 1
    total = sum(counts.values())
    return {'total': total, 'passed': counts['passed'], 'failed': counts['failed'],
            'skipped': counts['skipped'],
            'pass_rate_percent': round(counts['passed'] / total * 100, 1) if total else None}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', help='Path to a CSV with test_id and status columns')
    args = parser.parse_args()
    try:
        print(json.dumps(summarize(args.csv_file), indent=2))
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f'Error: {error}\n')

if __name__ == '__main__':
    main()
