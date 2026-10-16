"""Install pinned Studio skill payloads without executing installers or hooks."""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import urllib.request
import zipfile
from plugin_runtime import skills_directory, skill_state

LIMIT = 40 * 1024 * 1024

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Skill download redirected; installation stopped.')

def download(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Abacus-Studio-Skills'})
    with urllib.request.build_opener(NoRedirect).open(request, timeout=60) as response:
        payload = response.read(LIMIT + 1)
    if len(payload) > LIMIT:
        raise ValueError('Skill archive exceeds the installation limit.')
    return payload

def digest_directory(path):
    files = {}
    for child in sorted(path.rglob('*')):
        if child.is_symlink():
            raise ValueError('Managed skill contains a symbolic link.')
        if child.is_file():
            files[child.relative_to(path).as_posix()] = hashlib.sha256(child.read_bytes()).hexdigest()
    return files

def install(root, config, fetcher=download):
    root = Path(root).resolve()
    packages = config.get('skill_packages', [])
    if not isinstance(packages, list) or len(packages) > 20:
        raise ValueError('Invalid Studio skill catalog.')
    exclude = root / '.git/info/exclude'
    if exclude.is_symlink() or exclude.parent.is_symlink() or exclude.parent.parent.is_symlink():
        raise ValueError('Unsafe Git exclusions for local skill installation.')
    if packages and exclude.is_file():
        with exclude.open('a') as output:
            output.write(f'\n/{skills_directory()}/skills/\n/.studio/\n/.impeccable/\n')
    results = []
    for package in packages:
        if not isinstance(package, dict):
            raise ValueError('Invalid Studio skill package.')
        name, repository, commit, checksum, source = [package.get(key, '') for key in ('id', 'repository', 'commit', 'sha256', 'path')]
        license_path = package.get('license_path', 'LICENSE')
        if (not all(isinstance(v, str) for v in (name, repository, commit, checksum, source, license_path)) or
            not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', name) or
            not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository) or
            not re.fullmatch(r'[a-f0-9]{40}', commit) or not re.fullmatch(r'[a-f0-9]{64}', checksum) or
            any(part in ('', '.', '..') for part in source.split('/')) or source.startswith('/') or '\\' in source or
            license_path != 'LICENSE' or package.get('hooks') is not False):
            raise ValueError('Skill package is not a pinned, hook-free Studio source.')
        target = root / skills_directory() / 'skills' / name
        state = skill_state(root, name)
        for path in (target, target.parent, target.parent.parent, state, *state.parents):
            if path == root:
                break
            if path.is_symlink():
                raise ValueError('Skill installation paths must remain inside the workspace.')
        if target.exists():
            saved = json.loads(state.read_text()) if state.is_file() else {}
            if saved.get('commit') != commit or saved.get('files') != digest_directory(target):
                raise ValueError(f'Existing {name} skill preserved. Review the conflicting installation before retrying.')
            results.append({'id': name, 'state': 'already_installed', 'version': package.get('version')})
            continue
        payload = fetcher(f'https://codeload.github.com/{repository}/zip/{commit}')
        if len(payload) > LIMIT or hashlib.sha256(payload).hexdigest() != checksum:
            raise ValueError('Skill archive checksum did not match Studio. Nothing installed.')
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            prefix = f'{repository.split("/")[1]}-{commit}/'
            selected = {}
            total = 0
            for entry in archive.infolist():
                if entry.filename.startswith(prefix + source + '/'):
                    relative = entry.filename[len(prefix + source + '/'):]
                elif entry.filename == prefix + license_path:
                    relative = 'LICENSE'
                else:
                    continue
                if entry.is_dir():
                    continue
                path = PurePosixPath(relative)
                mode = entry.external_attr >> 16
                if (not relative or path.is_absolute() or '..' in path.parts or '\\' in relative or ':' in relative or
                    stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG)) or relative in selected):
                    raise ValueError('Unsafe skill archive. Nothing installed.')
                total += entry.file_size
                if total > LIMIT or len(selected) >= 1000:
                    raise ValueError('Skill payload exceeds the installation limit.')
                selected[relative] = entry
            if 'SKILL.md' not in selected or 'LICENSE' not in selected:
                raise ValueError('Skill entrypoint or license missing. Nothing installed.')
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix='.studio-skill-', dir=target.parent) as temporary:
                stage = Path(temporary) / name
                stage.mkdir()
                for relative, entry in selected.items():
                    path = stage / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(archive.read(entry))
                    path.chmod(0o755 if entry.external_attr >> 16 & 0o111 else 0o644)
                files = digest_directory(stage)
                state.parent.mkdir(parents=True, exist_ok=True)
                # Never merge into or overwrite a user-owned skill directory.
                if target.exists():
                    raise ValueError('Skill destination appeared during setup; nothing overwritten.')
                shutil.move(str(stage), str(target))
                state.write_text(json.dumps({'commit': commit, 'sha256': checksum, 'files': files}))
                state.chmod(0o600)
        results.append({'id': name, 'state': 'installed', 'version': package.get('version')})
    return results
