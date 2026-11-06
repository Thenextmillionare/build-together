"""Validate the canonical dataset before conversion to a training provider's format."""
import argparse
from collections import Counter
import json
from pathlib import Path


def validate(paths, require_splits=False):
    errors, counts, ids, scripts, groups = [], Counter(), set(), {}, {}
    total = 0
    for path in paths:
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            where = f'{path.name}:{line_number}'
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f'{where}: invalid JSON ({exc.msg})')
                continue
            if not isinstance(row, dict):
                errors.append(f'{where}: record must be an object')
                continue
            total += 1
            def text(obj, key):
                value = obj.get(key)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f'{where}: {key} must be nonempty text')
                    return ''
                return value.strip()
            identifier = text(row, 'id')
            if identifier in ids:
                errors.append(f'{where}: duplicate id {identifier}')
            ids.add(identifier)
            group = text(row, 'source_group')
            split = row.get('split')
            if split not in ('train', 'validation', 'test'):
                errors.append(f'{where}: split must be train, validation, or test')
            else:
                counts[split] += 1
                if group in groups and groups[group] != split:
                    errors.append(f'{where}: source_group {group} crosses splits')
                groups[group] = split
            objects = {}
            for key in ('source', 'review', 'input', 'target'):
                obj = row.get(key)
                if not isinstance(obj, dict):
                    errors.append(f'{where}: {key} must be an object')
                    obj = {}
                objects[key] = obj
            source, review, brief, target = (objects[k] for k in ('source', 'review', 'input', 'target'))
            if source.get('kind') not in ('original', 'licensed', 'permission'):
                errors.append(f'{where}: source.kind must be original, licensed, or permission')
            for key in ('reference', 'permission_note'):
                text(source, key)
            if source.get('approved_for_training') is not True:
                errors.append(f'{where}: source is not approved for training')
            if review.get('approved') is not True:
                errors.append(f'{where}: quality review is not approved')
            text(review, 'reviewer')
            for key in ('audience', 'objective', 'platform', 'tone', 'brief'):
                text(brief, key)
            duration = brief.get('duration_seconds')
            if type(duration) not in (int, float) or not 0 < duration < float('inf'):
                errors.append(f'{where}: duration_seconds must be a positive finite number')
            facts = brief.get('facts')
            if not isinstance(facts, list) or not all(isinstance(f, str) and f.strip() for f in facts):
                errors.append(f'{where}: facts must be a list of nonempty strings (or an empty list)')
            script = text(target, 'script')
            normalized = ' '.join(script.casefold().split())
            if normalized:
                if normalized in scripts:
                    errors.append(f'{where}: duplicate script (also in {scripts[normalized]})')
                scripts[normalized] = where
    if not total:
        errors.append('No dataset records found. Collect and review examples first.')
    if require_splits:
        for split in ('train', 'validation', 'test'):
            if not counts[split]:
                errors.append(f'No examples in {split} split')
    return errors, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).parents[1] / 'data')
    parser.add_argument('--require-splits', action='store_true')
    args = parser.parse_args()
    if not args.data_dir.is_dir():
        parser.error(f'Dataset directory does not exist: {args.data_dir}')
    errors, counts = validate(sorted(args.data_dir.glob('*.jsonl')), args.require_splits)
    print('Records by split:', dict(counts))
    for error in errors:
        print('ERROR:', error)
    if errors:
        raise SystemExit(1)
    print('Dataset structure passed. Human quality and permission review still apply.')


if __name__ == '__main__':
    main()
