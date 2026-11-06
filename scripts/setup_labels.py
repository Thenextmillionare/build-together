"""Create missing workspace labels; leave existing labels untouched."""
import json
import os
from pathlib import Path
import subprocess

repo = os.environ['GITHUB_REPOSITORY']
existing = set(json.loads(subprocess.check_output(['gh', 'label', 'list', '--repo', repo, '--limit', '1000', '--json', 'name', '--jq', '[.[].name]'])))
for label in json.loads(Path('.github/labels.json').read_text()):
    if label['name'] not in existing:
        subprocess.run(['gh', 'label', 'create', label['name'], '--repo', repo,
                        '--color', label['color'], '--description', label['description']], check=True)
        print('Created', label['name'])
    else:
        print('Already present:', label['name'])
