"""Clone a Studio-authorized repository into a new folder using OS Git credentials.

No tokens are accepted in the manifest or saved to a remote URL. Authentication
must already be provisioned by an approved credential helper outside this script.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def validate(manifest):
    if manifest.get('schema_version') != 1 or manifest.get('source_type') != 'git_clone':
        raise ValueError('Studio did not authorize a Git clone')
    repo = manifest.get('repository', '')
    branch = manifest.get('base_branch', '')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]*', branch) or '..' in branch or branch.endswith(('/', '.', '.lock')):
        raise ValueError('Invalid branch')
    if not re.fullmatch(r'[0-9a-fA-F]{40}', manifest.get('source_commit', '')):
        raise ValueError('Invalid revision')
    if not manifest.get('project_id') or any(k in manifest for k in ('token', 'password', 'download_url')):
        raise ValueError('Invalid clone authorization')
    return repo, branch


def clone(manifest, destination, run=subprocess.run):
    repo, branch = validate(manifest)
    destination = Path(destination).expanduser().absolute()
    if destination.exists() or destination.is_symlink() or not destination.parent.is_dir():
        raise ValueError('Choose a new folder in an existing directory')
    # Never execute checked-out hooks or fetch submodules. Credentials stay in the
    # approved OS helper. Git output may contain helper errors: do not print it.
    with tempfile.TemporaryDirectory(prefix='studio-empty-hooks-') as hooks:
        prefix = ['git', '-c', f'core.hooksPath={hooks}', '-c', 'protocol.file.allow=never']
        result = run(prefix + ['clone', '--single-branch', '--branch', branch,
                              '--no-recurse-submodules', '--',
                              f'https://github.com/{repo}.git', str(destination)],
                     capture_output=True, text=True, timeout=600)
    if result.returncode:
        raise ValueError('Clone failed')
    revision = run(['git', '-C', str(destination), 'rev-parse', 'HEAD'],
                   capture_output=True, text=True, timeout=20)
    if revision.returncode or revision.stdout.strip().lower() != manifest['source_commit'].lower():
        raise ValueError('Remote revision changed; obtain fresh Studio authorization')
    tracked = run(['git', '-C', str(destination), 'ls-files', '-z'],
                  capture_output=True, text=True, timeout=20)
    if tracked.returncode:
        raise ValueError('Could not inspect cloned files')
    for name in tracked.stdout.split('\0'):
        if not name:
            continue
        path = destination / name
        if name == '.gitmodules' or path.is_symlink():
            raise ValueError('Submodules and symlinks are unsupported by this pilot')
        if path.is_file():
            with path.open('rb') as content:
                if content.read(200).startswith(b'version https://git-lfs.github.com/spec/v1'):
                    raise ValueError('Git LFS assets need supported setup before preview')
    metadata = destination / '.studio'
    if metadata.exists() or metadata.is_symlink():
        raise ValueError('Repository contains reserved Studio metadata')
    metadata.mkdir(mode=0o700)
    saved = {k: manifest.get(k) for k in ('schema_version', 'project_id', 'repository',
                                        'base_branch', 'pr_target_branch', 'source_commit')}
    saved['source_type'] = 'git_clone'
    with (metadata / 'workspace.json').open('x') as output:
        json.dump(saved, output, indent=2)
    (metadata / 'workspace.json').chmod(0o600)
    return {'status': 'cloned', 'directory': str(destination), 'source_commit': revision.stdout.strip()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(clone(json.loads(sys.stdin.read(131072)), args.destination)))
        return 0
    except Exception:
        print('Clone did not complete. Check Git, authorized repository access, and the destination. Existing folders were not overwritten; a partial new folder may remain.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
