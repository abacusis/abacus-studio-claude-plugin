"""Check public README freshness; optionally require an update in a Git change set."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess


def validate(root, base=None):
    root = Path(root)
    readme = (root / 'README.md').read_text()
    version = json.loads((root / '.claude-plugin/plugin.json').read_text())['version']
    if f"### What's new in {version}" not in readme:
        raise ValueError('README latest-feature heading must match plugin version ' + version)
    for path in (root / 'agents').glob('*.md'):
        match = re.search(r'^# Abacus (.+)$', path.read_text(), re.M)
        if not match or match.group(1) not in readme:
            raise ValueError('README must introduce bundled specialist: ' + path.name)
    if base and set(base) != {'0'}:
        if not re.fullmatch(r'[a-fA-F0-9]{7,40}', base):
            raise ValueError('README comparison base must be a Git commit SHA')
        result = subprocess.run(['git', 'diff', '--name-only', base, '--', '.'],
                                cwd=root, capture_output=True, text=True, check=True)
        changed = result.stdout.splitlines()
        if changed and 'README.md' not in changed:
            raise ValueError('Every change set must update README.md with accurate client-facing value or a maintenance note')
    return version


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--base')
    group.add_argument('--base-env')
    args = parser.parse_args()
    base = args.base
    if args.base_env:
        base = os.environ.get(args.base_env)
        if not base:
            parser.error('Missing comparison base environment variable')
    try:
        version = validate(Path(__file__).resolve().parents[1], base)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, 'README check failed: ' + str(error) + '\n')
    print('README checked for ' + version + '; editorial review still required.')
