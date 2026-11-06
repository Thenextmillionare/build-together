import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location('dataset', ROOT / 'scripts/validate_dataset.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)

class DatasetTests(unittest.TestCase):
    def example(self):
        row = json.loads((ROOT / 'examples/format-example.jsonl').read_text())
        row['source']['approved_for_training'] = True
        row['review'] = {'approved': True, 'reviewer': 'test-fixture-reviewer'}
        return row

    def check_rows(self, rows, require_splits=False):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'examples.jsonl'
            path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
            return d.validate([path], require_splits)

    def test_empty_data_is_not_ready(self):
        errors, _ = d.validate([])
        self.assertTrue(any('No dataset records' in e for e in errors))

    def test_approved_record_passes(self):
        errors, counts = self.check_rows([self.example()])
        self.assertEqual(errors, [])
        self.assertEqual(counts['train'], 1)

    def test_documentation_example_cannot_be_used_as_approved_data(self):
        errors, _ = d.validate([ROOT / 'examples/format-example.jsonl'])
        self.assertTrue(any('not approved for training' in e for e in errors))
        self.assertTrue(any('quality review' in e for e in errors))

    def test_detects_leakage_and_duplicates(self):
        one = self.example()
        two = copy.deepcopy(one)
        two['split'] = 'test'
        errors, _ = self.check_rows([one, two])
        for fragment in ('duplicate id', 'duplicate script', 'crosses splits'):
            self.assertTrue(any(fragment in e for e in errors), fragment)

    def test_rejects_bad_types_without_crashing(self):
        row = self.example()
        row['source'] = []
        row['input']['duration_seconds'] = True
        row['input']['facts'] = 'not a list'
        errors, _ = self.check_rows([row, []])
        for fragment in ('source must be an object', 'duration_seconds', 'facts', 'record must be an object'):
            self.assertTrue(any(fragment in e for e in errors), fragment)

    def test_training_handoff_requires_all_splits(self):
        errors, _ = self.check_rows([self.example()], require_splits=True)
        self.assertTrue(any('validation split' in e for e in errors))
        self.assertTrue(any('test split' in e for e in errors))

if __name__ == '__main__':
    unittest.main()
