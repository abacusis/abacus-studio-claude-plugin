"""Install owned project-scoped Codex specialists; never alter global host config."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROLES = ('spec-writer', 'builder', 'verifier', 'code-reviewer', 'security-reviewer',
         'ui-reviewer', 'ux-reviewer', 'readiness-reviewer')


def sha(value):
    return hashlib.sha256(value).hexdigest()


def install(root, approved=False, package_root=None):
    if not approved:
        raise ValueError('Project specialist setup requires approval.')
    root = Path(root).resolve()
    package = Path(package_root or Path(__file__).resolve().parents[1]).resolve()
    if not (package / '.codex-plugin/plugin.json').is_file():
        raise ValueError('Use the packaged Codex adapter for specialist setup.')
    target = root / '.codex/agents'
    receipt = root / '.studio/codex-agents.json'
    for item in (root / '.codex', target, root / '.studio', receipt):
        if item.is_symlink():
            raise ValueError('Specialist setup refuses symbolic links.')
    if not root.is_dir() or not (root / '.studio').is_dir():
        raise ValueError('Complete Studio workspace setup first.')
    saved = json.loads(receipt.read_text()) if receipt.exists() else {}
    previous = saved.get('files', {})
    wanted = {}
    for role in ROLES:
        name = 'abacus-' + role
        instructions = (package / 'roles' / (role + '.md')).read_text().replace('<plugin-root>', str(package))
        instructions += ('\n\nUse only the coordinator-authorized scope. Do not spawn other agents. '
                         'Report unavailable tools or instructions; never bypass host permissions.\n')
        # JSON strings are valid TOML basic strings and avoid multiline quoting traps.
        content = (f'name = {json.dumps(name)}\n'
                   f'description = {json.dumps("Abacus " + role.replace("-", " ") + " specialist; use for a scoped handoff from the Engineering coordinator.")}\n'
                   f'developer_instructions = {json.dumps(instructions, ensure_ascii=False)}\n').encode()
        path = target / (name + '.toml')
        if path.is_symlink() or (path.exists() and (not path.is_file() or sha(path.read_bytes()) != previous.get(path.name))):
            raise ValueError(f'Existing {name} profile preserved. Resolve the conflict before setup.')
        wanted[path.name] = content
    # Preflight every profile before writing any. Preserve unrelated user profiles.
    resolved = subprocess.run(['git', '-C', str(root), 'rev-parse', '--git-path', 'info/exclude'],
                              check=True, capture_output=True, text=True).stdout.strip()
    exclude = Path(resolved)
    if not exclude.is_absolute():
        exclude = root / exclude
    if exclude.is_symlink() or exclude.parent.is_symlink():
        raise ValueError('Unsafe Git exclusions.')
    exclude.parent.mkdir(parents=True, exist_ok=True)
    with exclude.open('a') as stream:
        stream.write('\n/.codex/agents/abacus-*.toml\n/.studio/\n')
    target.mkdir(parents=True, exist_ok=True)
    for name, content in wanted.items():
        path = target / name
        if not path.exists() or path.read_bytes() != content:
            temporary = path.with_suffix('.studio-tmp')
            with temporary.open('xb') as stream:
                stream.write(content)
            temporary.replace(path)
    receipt.write_text(json.dumps({'schema_version': 1, 'files': {name: sha(value) for name, value in wanted.items()}}, indent=2) + '\n')
    receipt.chmod(0o600)
    return {'status': 'installed', 'profiles': ['abacus-' + role for role in ROLES],
            'restart_required': True, 'global_configuration_changed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--approved', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.workspace, args.approved)))
    except Exception as error:
        parser.exit(1, str(error) + '\n')
