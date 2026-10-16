"""Prepare a fresh, allowlisted distribution folder and verified ZIP; never publish."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
import zipfile

ROOT_FILES = {'.gitignore', '.mcp.json', 'README.md', 'INSTALL.md', 'SECURITY.md', 'RELEASE.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md'}
PATTERNS = ('.claude-plugin/*.json', 'agents/*.md', 'skills/*/SKILL.md', 'references/*.md',
            'references/*/*.md', 'scripts/*.py', 'scripts/requirements.txt',
            'tests/*.py', 'tests/*.mjs')
FORBIDDEN = {'.git', '.claude', '.studio', '.impeccable', '__pycache__', 'node_modules'}
CONCRETE_SECRET = re.compile(r'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----|\b(?:sbp_[A-Za-z0-9]{20,}|sb_secret_[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})\b|\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}')

def release_files(root):
    root = Path(root).resolve()
    selected = {root / name for name in ROOT_FILES}
    for pattern in PATTERNS:
        selected.update(root.glob(pattern))
    files = []
    for path in sorted(selected):
        relative = path.relative_to(root)
        if any(part in FORBIDDEN for part in relative.parts) or relative.name.startswith('.env'):
            raise ValueError('Forbidden release path: ' + relative.as_posix())
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root and root in parent.parents):
            raise ValueError('Release symlink refused: ' + relative.as_posix())
        if not path.is_file():
            raise ValueError('Required release file missing: ' + relative.as_posix())
        if CONCRETE_SECRET.search(path.read_text()):
            raise ValueError('Possible credential; inspect privately: ' + relative.as_posix())
        files.append(path)
    return files

def build(root, output):
    root, output = Path(root).resolve(), Path(output).absolute()
    archive = output.with_name(output.name + '.zip')
    if output.exists() or output.is_symlink() or archive.exists() or archive.is_symlink() or not output.parent.is_dir():
        raise ValueError('Choose a NEW folder with an existing parent; nothing overwritten.')
    if output == root or root in output.parents:
        raise ValueError('Release output must be outside the source folder.')
    files = release_files(root)
    manifest = {'version': json.loads((root / '.claude-plugin/plugin.json').read_text())['version'],
                'repository': 'abacusis/abacus-studio-claude-plugin', 'files': {},
                'excluded': 'Everything outside the distribution allowlist, including local Claude settings, caches, credentials and Git history.',
                'publication_performed': False}
    output.mkdir()
    for source in files:
        relative = source.relative_to(root)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        target.chmod(0o755 if source.stat().st_mode & 0o111 else 0o644)
        manifest['files'][relative.as_posix()] = hashlib.sha256(target.read_bytes()).hexdigest()
    (output / 'RELEASE-MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundled:
        for path in sorted(output.rglob('*')):
            if path.is_file():
                bundled.write(path, path.relative_to(output).as_posix())
    with zipfile.ZipFile(archive) as bundled:
        if bundled.testzip() is not None:
            raise ValueError('ZIP integrity check failed.')
        if set(bundled.namelist()) != set(manifest['files']) | {'RELEASE-MANIFEST.json'}:
            raise ValueError('ZIP contains unexpected files.')
        for name, digest in manifest['files'].items():
            if hashlib.sha256(bundled.read(name)).hexdigest() != digest:
                raise ValueError('ZIP checksum mismatch: ' + name)
    return {'folder': str(output), 'zip': str(archive), 'files': len(manifest['files']),
            'version': manifest['version'], 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest()}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(build(Path(__file__).resolve().parents[1], args.output), indent=2))
