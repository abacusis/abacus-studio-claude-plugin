"""Download a Studio-prepared ZIP safely. JSON from stdin; never execute repo code."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import urllib.request
from urllib.parse import urlparse
import zipfile

MAX_DOWNLOAD = 100 * 1024 * 1024
MAX_EXPANDED = 512 * 1024 * 1024

def validate_manifest(manifest):
    if manifest.get('schema_version') != 1 or manifest.get('archive_format') != 'zip':
        raise ValueError('Unsupported workspace download format.')
    repo, sha = manifest.get('repository', ''), manifest.get('source_commit', '')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo) or not re.fullmatch(r'[a-fA-F0-9]{40}', sha):
        raise ValueError('Invalid repository or source revision.')
    url = urlparse(manifest.get('download_url', ''))
    if url.scheme != 'https' or url.netloc != 'codeload.github.com' or url.fragment or url.path not in (
        f'/{repo}/legacy.zip/{sha}', f'/{repo}/zip/{sha}'
    ):
        raise ValueError('Download is not a trusted GitHub source archive.')
    expiry = datetime.datetime.fromisoformat(manifest['expires_at'].replace('Z', '+00:00'))
    if expiry <= datetime.datetime.now(datetime.timezone.utc):
        raise ValueError('Download expired. Request a fresh download from Studio.')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Unexpected download redirect. Request a fresh download from Studio.')

def archive_entries(archive):
    entries = archive.infolist()
    if not entries or len(entries) > 20000 or sum(entry.file_size for entry in entries) > MAX_EXPANDED:
        raise ValueError('Archive is empty or exceeds safe extraction limits.')
    roots, seen, files = set(), set(), []
    for entry in entries:
        name = entry.filename
        parts = PurePosixPath(name).parts
        if not parts or name.startswith('/') or '\\' in name or ':' in name or any(p in ('..', '.') for p in parts):
            raise ValueError('Unsafe archive path.')
        roots.add(parts[0])
        mode = entry.external_attr >> 16
        if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
            raise ValueError('Archive links and special files are not supported.')
        relative = Path(*parts[1:])
        if not parts[1:] or entry.is_dir():
            continue
        if any(p.lower() in ('.git', '.studio') for p in parts[1:]) or relative.name == '.gitmodules':
            raise ValueError('Git metadata, submodules, and reserved workspace paths are not supported.')
        key = str(relative).casefold()
        if key in seen or entry.flag_bits & 1 or entry.file_size > 128 * 1024 * 1024:
            raise ValueError('Archive has duplicate, encrypted, or oversized files.')
        seen.add(key)
        files.append((entry, relative))
    if len(roots) != 1 or not files:
        raise ValueError('Expected one repository root in the source archive.')
    return files

def extract_workspace(archive_path, manifest, destination):
    destination = Path(destination).expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError('Destination already exists. Choose a new folder; nothing was overwritten.')
    if not destination.parent.is_dir():
        raise ValueError('Choose a folder inside an existing parent directory.')
    with zipfile.ZipFile(archive_path) as archive:
        files = archive_entries(archive)
        # Validate LFS and CRC before creating the destination. Do not present pointers as code.
        for entry, _ in files:
            with archive.open(entry) as content:
                first = content.read(200)
                if first.startswith(b'version https://git-lfs.github.com/spec/v1'):
                    raise ValueError('This app uses Git LFS. Archive setup cannot fetch its assets yet.')
                while content.read(1024 * 1024):
                    pass
        destination.mkdir(mode=0o700)  # Exclusive creation; no existing user folder is reused.
        hashes = {}
        for entry, relative in files:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            digest = hashlib.sha256()
            with archive.open(entry) as source, target.open('xb') as output:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    output.write(chunk)
                    digest.update(chunk)
            target.chmod(0o700 if (entry.external_attr >> 16) & 0o111 else 0o600)
            hashes[relative.as_posix()] = digest.hexdigest()
        metadata = destination / '.studio'
        metadata.mkdir(mode=0o700)
        # Explicit allowlist: never persist the temporary download URL or credentials.
        saved = {key: manifest.get(key) for key in ('schema_version', 'project_id', 'repository', 'base_branch', 'pr_target_branch', 'source_commit')}
        saved.update({'source_type': 'github_archive', 'baseline_file_sha256': hashes})
        with (metadata / 'workspace.json').open('x') as output:
            json.dump(saved, output, indent=2)
        (metadata / 'workspace.json').chmod(0o600)
    return destination

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    try:
        manifest = json.loads(sys.stdin.read(128 * 1024))
        validate_manifest(manifest)
        destination = Path(args.destination).expanduser().absolute()
        if destination.exists() or destination.is_symlink():
            raise ValueError('Destination already exists. Choose a new folder; nothing was overwritten.')
        with tempfile.TemporaryDirectory(prefix='studio-source-') as temporary:
            archive_path = Path(temporary) / 'source.zip'
            opener = urllib.request.build_opener(NoRedirect)
            with opener.open(manifest['download_url'], timeout=60) as response, archive_path.open('xb') as output:
                size = 0
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > MAX_DOWNLOAD:
                        raise ValueError('Download exceeds the 100 MB limit.')
                    output.write(chunk)
            path = extract_workspace(archive_path, manifest, destination)
        print(json.dumps({'status': 'downloaded', 'directory': str(path), 'source_commit': manifest['source_commit']}))
    except Exception:
        # HTTP exceptions can contain signed URLs. Never print them or stack traces.
        print('Workspace download failed. Check the destination, archive compatibility, and link expiry. Existing folders are never overwritten. A partially created new folder may remain; choose another folder or inspect it before retrying.', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
