import tempfile
import unittest
from pathlib import Path
from summary import summarize

class SummaryTests(unittest.TestCase):
    def write_csv(self, text):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / 'results.csv'
        path.write_text(text, encoding='utf-8')
        return path

    def test_counts_and_rate(self):
        result = summarize(self.write_csv('test_id,status\na,passed\nb,failed\nc,skipped\n'))
        self.assertEqual(result, {'total': 3, 'passed': 1, 'failed': 1, 'skipped': 1, 'pass_rate_percent': 33.3})

    def test_empty_file_with_headers(self):
        self.assertIsNone(summarize(self.write_csv('test_id,status\n'))['pass_rate_percent'])

    def test_invalid_status_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'line 2'):
            summarize(self.write_csv('test_id,status\na,unknown\n'))

    def test_missing_columns_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'columns'):
            summarize(self.write_csv('id,status\na,passed\n'))

if __name__ == '__main__':
    unittest.main()
