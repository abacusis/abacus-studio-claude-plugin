"""Write authorized Studio sandbox values locally; never return their values."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

NAMES = {'VITE_SUPABASE_URL', 'VITE_SUPABASE_PUBLISHABLE_KEY', 'VITE_SUPABASE_PROJECT_ID',
         'SUPABASE_URL', 'SUPABASE_PUBLISHABLE_KEY', 'SUPABASE_PROJECT_ID', 'SUPABASE_SECRET_KEY'}
START = '# BEGIN STUDIO SANDBOX\n'
END = '# END STUDIO SANDBOX\n'


def provision(root, project, config, operation, git):
    root = Path(root).resolve()
    payload = operation(project, 'environment')
    values = payload.get('environment')
    if not isinstance(values, dict) or set(values) - NAMES or any(
            not isinstance(value, str) or any(char in value for char in '\r\n\x00') for value in values.values()):
        raise ValueError('Studio returned an unsupported sandbox environment.')
    if not values:
        return []
    if 'SUPABASE_SECRET_KEY' in values and not re.fullmatch(r'sb_secret_[A-Za-z0-9_-]{20,200}', values['SUPABASE_SECRET_KEY']):
        raise ValueError('Studio returned an invalid sandbox server secret.')
    refs = {service.get('project_ref') for service in config.get('sandbox_services', []) if service.get('kind') == 'supabase'}
    ref = values.get('VITE_SUPABASE_PROJECT_ID')
    if ref not in refs or not re.fullmatch(r'[a-z0-9]{20}', ref or '') or values.get('VITE_SUPABASE_URL') != f'https://{ref}.supabase.co':
        raise ValueError('Sandbox environment does not match Studio configuration.')
    # Only alias public values requested by this app's Studio configuration.
    # Never map the privileged server secret to a browser-visible variable.
    values = dict(values)
    aliases = {'NEXT_PUBLIC_SUPABASE_URL': 'VITE_SUPABASE_URL',
               'NEXT_PUBLIC_SUPABASE_ANON_KEY': 'VITE_SUPABASE_PUBLISHABLE_KEY',
               'NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY': 'VITE_SUPABASE_PUBLISHABLE_KEY'}
    for name, source in aliases.items():
        if name in config.get('required_env_names', []):
            if source not in values:
                raise ValueError('Studio sandbox public connection is incomplete.')
            values[name] = values[source]
    if any(name in os.environ and os.environ[name] != value for name, value in values.items()):
        raise ValueError('Inherited environment values conflict with the Studio sandbox; nothing overwritten.')
    for override in root.glob('.env.*'):
        if override.name == '.env.example':
            continue
        if override.is_symlink():
            raise ValueError('Local environment overrides must remain inside the workspace.')
        if override.is_file() and any(re.search(rf'^\s*(?:export\s+)?{name}\s*=', override.read_text(), re.M) for name in values):
            raise ValueError('A local environment override conflicts with Studio sandbox setup; nothing overwritten.')
    if git.text('ls-files', '--', '.env'):
        raise ValueError('The repository tracks .env. Remove it before automatic sandbox setup.')
    path, state = root / '.env', root / '.studio/environment.json'
    if path.is_symlink() or state.is_symlink() or state.parent.is_symlink():
        raise ValueError('Sandbox environment files must remain inside the workspace.')
    old = path.read_text() if path.exists() else ''
    block = START + ''.join(f'{name}={json.dumps(value)}\n' for name, value in sorted(values.items())) + END
    if START in old or END in old:
        if old.count(START) != 1 or old.count(END) != 1:
            raise ValueError('Local sandbox settings were edited. Preserve them and ask the administrator to review setup.')
        begin, finish = old.index(START), old.index(END) + len(END)
        previous = old[begin:finish]
        saved = json.loads(state.read_text()) if state.exists() else {}
        if saved.get('digest') != hashlib.sha256(previous.encode()).hexdigest():
            raise ValueError('Local sandbox settings were edited; nothing overwritten.')
        outside = old[:begin] + old[finish:]
        replacement = old[:begin] + block + old[finish:]
    else:
        outside = old
        replacement = old + ('\n' if old and not old.endswith('\n') else '') + block
    if any(re.search(rf'^\s*(?:export\s+)?{name}\s*=', outside, re.M) for name in values):
        raise ValueError('Existing local environment values conflict with Studio sandbox setup; nothing overwritten.')
    # Local exclusion is installed before writing values, regardless of repo rules.
    exclude = root / '.git/info/exclude'
    if exclude.is_symlink():
        raise ValueError('Unsafe Git exclusion configuration.')
    with exclude.open('a') as output:
        output.write('\n/.env\n/.studio/\n/.claude/\n')
    descriptor, temporary = tempfile.mkstemp(prefix='.studio-env-', dir=root)
    try:
        with os.fdopen(descriptor, 'w') as output:
            output.write(replacement)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    state.parent.mkdir(exist_ok=True, mode=0o700)
    state.write_text(json.dumps({'names': sorted(values), 'digest': hashlib.sha256(block.encode()).hexdigest()}))
    state.chmod(0o600)
    return sorted(values)
