"""Regenerate owned tool packages on the shared source branch; never publish."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from build_release import render_target, release_files, CONCRETE_SECRET

MARKER = 'GENERATED-FILES.json'
HOSTS = ('claude', 'codex')


def expected(root):
    sources = release_files(root)
    return {host: render_target(root, host, sources) for host in HOSTS}


def digest(value):
    return hashlib.sha256(value).hexdigest()


def safe_name(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or '..' in path.parts or '\\' in name or path.as_posix() != name:
        raise ValueError('Unsafe generated filename')
    return path


def prepare(root, host, wanted):
    target = root / 'plugins' / host
    for path in (target.parent, target):
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError('Generated package path must be a real directory')
    for name, value in wanted.items():
        safe_name(name)
        if name == MARKER or CONCRETE_SECRET.search(value.decode()):
            raise ValueError('Unsafe generated content')
    current = {}
    if target.exists():
        for path in target.rglob('*'):
            if path.is_symlink():
                raise ValueError('Generated package contains a symlink; nothing overwritten')
            if path.is_file():
                current[path.relative_to(target).as_posix()] = path.read_bytes()
            elif not path.is_dir():
                raise ValueError('Unsupported generated path')
    marker = current.pop(MARKER, None)
    saved = json.loads(marker) if marker else None
    actual = {name: digest(value) for name, value in current.items()}
    if saved is not None:
        if saved.get('schema_version') != 1 or saved.get('files') != actual:
            raise ValueError('Generated package has local edits; preserve/review them before regenerating')
    elif current:
        raise ValueError('Existing package has no ownership manifest; nothing overwritten')
    manifest = {'schema_version': 1, 'generator': 'scripts/generate_packages.py',
                'files': {name: digest(value) for name, value in sorted(wanted.items())}}
    marker_bytes = (json.dumps(manifest, indent=2) + '\n').encode()
    fresh = current == wanted and marker == marker_bytes
    return target, wanted, current, marker_bytes, fresh


def sync(root, check=False):
    root = Path(root).resolve()
    desired = expected(root)
    # Preflight ALL targets before any writes, including local-edit/symlink checks.
    plans = {host: prepare(root, host, desired[host]) for host in HOSTS}
    stale = [host for host, plan in plans.items() if not plan[4]]
    if check and stale:
        raise ValueError('Packages stale: ' + ', '.join(stale) + '. Run python3 scripts/generate_packages.py')
    if not check:
        for target, wanted, current, marker_bytes, fresh in plans.values():
            if fresh:
                continue
            # Only manifest-owned stale files can be removed; never clear folders.
            for name in set(current) - set(wanted):
                (target / safe_name(name)).unlink()
            for name, value in wanted.items():
                path = target / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(value)
                path.chmod(0o644)
            (target / MARKER).write_bytes(marker_bytes)
    return {'status': 'generated' if stale else 'current',
            'packages': {host: len(desired[host]) for host in HOSTS}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(sync(Path(__file__).resolve().parents[1], args.check)))
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')
