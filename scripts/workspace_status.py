"""Read-only status for Studio source snapshots. Never prints source content."""
import argparse
import json
from pathlib import Path
import sys

from sync_workspace import snapshot, excluded


def status(root):
    root = Path(root).resolve()
    metadata = json.loads((root / '.studio/workspace.json').read_text())
    baseline = metadata.get('baseline_file_sha256')
    if not isinstance(baseline, dict):
        raise ValueError('Missing snapshot baseline')
    # Use the same exclusions and secret checks as the upload prototype.
    hashes, _ = snapshot(root)
    baseline = {path: digest for path, digest in baseline.items() if not excluded(path)}
    return {'status': 'submission_blocked',
            'reason': 'This workspace is a source snapshot. An authorized client Git repository must be configured before submission.',
            'added': sorted(set(hashes) - set(baseline)),
            'modified': sorted(p for p in hashes.keys() & baseline.keys() if hashes[p] != baseline[p]),
            'deleted': sorted(set(baseline) - set(hashes))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(status(args.workspace)))
        return 0
    except Exception:
        print('Status could not be checked safely. Check workspace metadata and excluded or unsupported files.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
