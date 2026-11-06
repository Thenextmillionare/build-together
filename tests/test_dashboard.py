from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('dashboard', Path(__file__).parents[1] / 'scripts/dashboard.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
NOW = datetime(2026, 11, 6, 18, tzinfo=timezone.utc)

def issue(number, tags=(), **overrides):
    result = dict(number=number, title='A task', state='open', labels=[{'name': t} for t in tags],
                  created_at='2026-10-01T00:00:00Z', updated_at='2026-10-25T00:00:00Z', assignees=[])
    result.update(overrides)
    return result

class DashboardTests(unittest.TestCase):
    def test_empty_workspace(self):
        report = d.render([], 'owner/repo', NOW)
        self.assertIn('| 0 | 0 | 0 | 0 |', report)
        self.assertIn('No work logs yet.', report)

    def test_counts_exclude_prs_and_not_planned(self):
        rows = [issue(1, ['type:task', 'status:blocked']), issue(2, ['type:review', 'status:review']),
                issue(3, ['type:task'], pull_request={}),
                issue(4, ['type:task'], state='closed', closed_at='2026-11-05T00:00:00Z', state_reason='completed'),
                issue(5, ['type:task'], state='closed', closed_at='2026-11-05T00:00:00Z', state_reason='not_planned')]
        self.assertIn('| 1 | 1 | 1 | 1 |', d.render(rows, 'owner/repo', NOW))

    def test_stale_boundary_and_comments(self):
        old = issue(1, ['type:task', 'status:doing'], updated_at='2026-10-30T18:00:00Z')
        recent = issue(2, ['type:task', 'status:doing'], updated_at='2026-11-06T00:00:00Z')
        section = d.render([old, recent], 'owner/repo', NOW).split('## Worth checking in on')[1].split('## Tracking')[0]
        self.assertIn('#1', section)
        self.assertNotIn('#2', section)

    def test_conflicting_and_missing_status(self):
        rows = [issue(1, ['type:task']), issue(2, ['type:task', 'status:doing', 'status:next']), issue(3, ['type:task', 'status:next'])]
        section = d.render(rows, 'owner/repo', NOW).split('## Tracking needs a quick fix')[1]
        self.assertIn('#1', section)
        self.assertIn('#2', section)
        self.assertNotIn('#3', section)

    def test_titles_cannot_inject_markdown_or_html(self):
        report = d.render([issue(1, ['type:task'], title='x | [click](https://evil.example)\n<img src=x>')], 'owner/repo', NOW)
        self.assertNotIn('<img', report)
        self.assertIn(r'\|', report)
        self.assertIn(r'\[click\]', report)
        self.assertIn('https://github.com/owner/repo/issues/1', report)

    def test_fetch_paginates_and_filters_prs(self):
        from unittest.mock import patch, MagicMock
        pages = [[issue(n) for n in range(99)] + [issue(99, pull_request={})], [issue(100)]]
        responses = []
        import json
        import io
        for page in pages:
            response = MagicMock()
            response.__enter__.return_value = io.StringIO(json.dumps(page))
            responses.append(response)
        with patch.object(d.urllib.request, 'urlopen', side_effect=responses) as request:
            result = d.fetch_issues('owner/repo', 'test-token')
        self.assertEqual(len(result), 100)
        self.assertIn('page=2', request.call_args.args[0].full_url)

if __name__ == '__main__':
    unittest.main()
