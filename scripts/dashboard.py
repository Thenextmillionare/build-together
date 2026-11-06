"""Render a GitHub Issues snapshot. Python standard library only."""
import argparse
from datetime import datetime, timezone, timedelta
import html
import json
import os
from pathlib import Path
import re
import urllib.request

STATUSES = ('status:next', 'status:doing', 'status:blocked', 'status:review')

def fetch_issues(repo, token):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Repository must be owner/name')
    result = []
    page = 1
    while True:
        req = urllib.request.Request(
            f'https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}',
            headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
                     'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'build-together-dashboard'})
        with urllib.request.urlopen(req, timeout=30) as response:
            batch = json.load(response)
        result.extend(i for i in batch if 'pull_request' not in i)
        if len(batch) < 100:
            return result
        page += 1

def labels(issue):
    return {v if isinstance(v, str) else v['name'] for v in issue.get('labels', [])}

def safe(value):
    # Render issue text literally: Markdown/HTML in a title must not alter the report.
    value = ' '.join(str(value).split())
    value = html.escape(value)
    return re.sub(r'([\\`*_{}\[\]()|!#])', r'\\\1', value)

def render(issues, repo, now=None):
    now = now or datetime.now(timezone.utc)
    issues = [i for i in issues if 'pull_request' not in i]
    active = [i for i in issues if i['state'] == 'open']
    tasks = [i for i in active if 'type:task' in labels(i)]
    blocked = [i for i in active if 'status:blocked' in labels(i)]
    reviews = [i for i in active if 'type:review' in labels(i) or 'status:review' in labels(i)]
    logs = sorted((i for i in issues if 'type:log' in labels(i)), key=lambda i: i['created_at'], reverse=True)[:10]
    closed = [i for i in issues if i['state'] == 'closed' and 'type:task' in labels(i)
              and i.get('state_reason') != 'not_planned' and i.get('closed_at')
              and datetime.fromisoformat(i['closed_at'].replace('Z', '+00:00')) >= now-timedelta(days=7)]
    stale = [i for i in tasks if datetime.fromisoformat(i['updated_at'].replace('Z', '+00:00')) <= now-timedelta(days=7)]
    needs_status = [i for i in tasks if len(labels(i).intersection(STATUSES)) != 1]
    lines = ['# Progress dashboard', '', '> One shared view of the work. Issues are the source of truth.', '',
             f'**Snapshot:** {now:%Y-%m-%d %H:%M UTC} · [All issues](https://github.com/{repo}/issues) · [Pull requests](https://github.com/{repo}/pulls)', '',
             '| Open tasks | Blocked items | Awaiting input | Tasks completed · 7 days |',
             '| :---: | :---: | :---: | :---: |',
             f'| {len(tasks)} | {len(blocked)} | {len(reviews)} | {len(closed)} |', '']
    def section(title, rows, empty):
        lines.extend([f'## {title}', ''])
        if not rows:
            lines.extend([empty, ''])
            return
        lines.extend(['| Item | Next action owner | Status | Updated |', '| :--- | :--- | :--- | :--- |'])
        for i in sorted(rows, key=lambda i: i['updated_at'], reverse=True):
            owner = ', '.join(safe(a['login']) for a in i.get('assignees', [])) or 'Unassigned'
            status = ', '.join(safe(s.removeprefix('status:')) for s in STATUSES if s in labels(i)) or safe(i['state'])
            # Construct links from validated repo and numeric issue IDs, not issue-supplied URLs.
            number = int(i['number'])
            lines.append(f"| [#{number} · {safe(i['title'])}](https://github.com/{repo}/issues/{number}) | {owner} | {status} | {i['updated_at'][:10]} |")
        lines.append('')
    section('Active work', tasks, 'No open tasks yet. Pick a first outcome together and create a Task issue.')
    section('Blockers', blocked, 'No blockers recorded.')
    section('Feedback queue', reviews, 'No pending feedback requests.')
    section('Recent work logs', logs, 'No work logs yet. Add one after your first session.')
    section('Worth checking in on · 7+ days without activity', stale, 'No stale tasks.')
    section('Tracking needs a quick fix', needs_status, 'All open tasks have exactly one status label.')
    lines.extend(['---', '', '**Reading this snapshot:** comments count as updates. Completed tasks exclude issues closed as not planned. Categories may overlap. No due dates are inferred. If this timestamp looks old, check the Refresh dashboard workflow in Actions.', '',
                  '[Home](README.md) · [How we work](docs/WORKFLOW.md)', ''])
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY', 'Thenextmillionare/build-together'))
    parser.add_argument('--input', type=Path, help='Offline issue snapshot JSON')
    parser.add_argument('--output', type=Path, default=Path('DASHBOARD.md'))
    args = parser.parse_args()
    issues = json.loads(args.input.read_text()) if args.input else fetch_issues(args.repo, os.environ['GH_TOKEN'])
    args.output.write_text(render(issues, args.repo))

if __name__ == '__main__':
    main()
