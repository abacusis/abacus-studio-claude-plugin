"""Opt-in pilot watcher. Token from stdin stays in memory; no GitHub credentials."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import stat
import sys
import time
import urllib.error
import urllib.request
import uuid

EXCLUDED_DIRS = {'.git', '.studio', '.claude', '.impeccable', '.github', 'node_modules', 'dist', 'build',
                 'coverage', '.netlify', '.next', '.output', '.cache', '.tanstack', '.vite',
                 '.turbo', '.svelte-kit', '.vscode', '__pycache__', '.venv'}
SECRET_PATH = re.compile(r'^(\.env(?:\..*)?|.*\.(pem|key|p12|pfx|log|tsbuildinfo)|credentials(?:\..*)?|id_rsa|id_ed25519|\.npmrc|\.pypirc|\.gitmodules|\.DS_Store)$', re.I)
SECRET = re.compile(r'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----|\b(?:sbp_[A-Za-z0-9]{20,}|sb_secret_[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16}|sk-(?:proj-)?[A-Za-z0-9_-]{24,})\b|(?:password|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*["\'][^"\'\r\n]{12,}["\']', re.I)

def excluded(path):
    parts = Path(path).parts
    return any(p.lower() in EXCLUDED_DIRS for p in parts) or bool(SECRET_PATH.match(parts[-1]))

def snapshot(root):
    hashes, content = {}, {}
    for folder, directories, files in os.walk(root, followlinks=False):
        directories[:] = [d for d in directories if d.lower() not in EXCLUDED_DIRS]
        if any((Path(folder) / d).is_symlink() for d in directories):
            raise ValueError('Symlink directory needs attention.')
        for name in files:
            source = Path(folder) / name
            relative = source.relative_to(root).as_posix()
            if excluded(relative):
                continue
            if source.is_symlink() or not source.is_file():
                raise ValueError('Symlink or special file needs attention.')
            # Open without following symlinks where supported; verify the handle too.
            fd = os.open(source, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
            with os.fdopen(fd, 'rb') as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    raise ValueError('Special file needs attention.')
                raw = stream.read(1_000_001)
                digest = hashlib.sha256(raw)
                for chunk in iter(lambda: stream.read(1_000_000), b''):
                    digest.update(chunk)
            hashes[relative] = digest.hexdigest()
            try:
                text = raw.decode('utf-8')
                content[relative] = text if len(raw) <= 1_000_000 and '\0' not in text else None
            except UnicodeDecodeError:
                content[relative] = None
    return hashes, content

def changes(baseline, hashes, content):
    files = []
    for path in sorted(set(baseline) | set(hashes)):
        if excluded(path) or baseline.get(path) == hashes.get(path):
            continue
        if len(path) > 240 or not re.fullmatch(r'[A-Za-z0-9_. /@()+-]+', path):
            raise ValueError('A changed path is outside the pilot supported paths.')
        if path in hashes and content[path] is None:
            raise ValueError('Changed binary or oversized file: pilot sync supports small text changes only.')
        text = content.get(path)
        if text is not None and SECRET.search(text):
            raise ValueError('Possible secret detected. Sync paused; changes remain local.')
        files.append({'path': path, 'content': text})
    if len(files) > 100 or sum(len((f['content'] or '').encode()) for f in files) > 1_000_000:
        raise ValueError('Checkpoint exceeds pilot size limits. Changes remain local.')
    return files

def write_state(path, state):
    if path.is_symlink():
        raise ValueError('Unsafe sync state path.')
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex)
    fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, 'w') as output:
        json.dump(state, output)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Sync endpoint redirected; stopped to protect authorization.')

def request(grant, body):
    # Pinned Studio backend, never a URL supplied by repository content.
    if grant.get('endpoint') != 'https://aseymhsdlzcwquwcbxzc.supabase.co/functions/v1/local-sync':
        raise ValueError('Untrusted Studio sync endpoint.')
    req = urllib.request.Request(grant['endpoint'], data=json.dumps(body).encode(),
        headers={'Authorization': 'Bearer ' + grant['token'], 'Content-Type': 'application/json'}, method='POST')
    opener = urllib.request.build_opener(NoRedirect)
    with opener.open(req, timeout=30) as response:
        return json.loads(response.read(100_000))

def run(root, grant, interval=3, quiet=10):
    metadata = root / '.studio'
    if root.is_symlink() or metadata.is_symlink() or not metadata.is_dir():
        raise ValueError('Use a Studio-downloaded workspace.')
    manifest_path = metadata / 'workspace.json'
    if manifest_path.is_symlink():
        raise ValueError('Unsafe workspace metadata.')
    manifest = json.loads(manifest_path.read_text())
    if manifest['source_commit'] != grant['source_commit'] or manifest['project_id'] != grant['project_id']:
        raise ValueError('Sync grant does not match the downloaded snapshot.')
    lock = metadata / 'sync-running'
    lock.mkdir()  # One process per workspace; stale lock needs explicit recovery.
    state_path = metadata / 'sync-state.json'
    try:
        if state_path.is_symlink():
            raise ValueError('Unsafe sync state path.')
        state = json.loads(state_path.read_text()) if state_path.exists() else {
            'workspace_id': grant['workspace_id'], 'head': grant['source_commit'],
            'baseline': manifest['baseline_file_sha256'], 'pending': None}
        if state['workspace_id'] != grant['workspace_id']:
            raise ValueError('Existing sync state belongs to another working branch. Do not reset it automatically.')
        previous, stable_at = None, time.monotonic()
        while True:
            try:
                hashes, content = snapshot(root)
                if hashes != previous:
                    previous, stable_at = hashes, time.monotonic()
                pending = state.get('pending')
                if not pending and time.monotonic() - stable_at >= quiet:
                    files = changes(state['baseline'], hashes, content)
                    if files:
                        pending = {'action': 'checkpoint', 'request_id': str(uuid.uuid4()),
                                   'expected_head': state['head'], 'files': files}
                        state['pending'] = pending
                        write_state(state_path, state)  # Persist same request ID before sending.
                if pending:
                    request(grant, pending)
                    status = request(grant, {'action': 'status'})
                    job = status.get('job')
                    if not job or job['id'] != pending['request_id']:
                        raise ValueError('Checkpoint status mismatch; needs attention.')
                    if job['state'] == 'blocked':
                        raise ValueError('Checkpoint needs attention; no force push or automatic reset.')
                    if job['state'] == 'done':
                        for file in pending['files']:
                            if file['content'] is None:
                                state['baseline'].pop(file['path'], None)
                            else:
                                state['baseline'][file['path']] = hashlib.sha256(file['content'].encode()).hexdigest()
                        state.update(head=job['target_commit'], pending=None)
                        write_state(state_path, state)
                        print(json.dumps({'status': 'saved_to_studio', 'commit_url': job['commit_url']}), flush=True)
                    else:
                        print(json.dumps({'status': 'pending'}), flush=True)
                time.sleep(interval)
            except urllib.error.HTTPError as cause:
                if cause.code < 500 and cause.code != 429:
                    raise ValueError('Access or checkpoint needs attention.') from None
                print(json.dumps({'status': 'pending', 'message': 'Studio unavailable; retrying the same checkpoint.'}), flush=True)
                time.sleep(max(interval, 15))
            except (urllib.error.URLError, TimeoutError):
                print(json.dumps({'status': 'offline_or_access_unavailable', 'message': 'Changes remain local; retrying the same checkpoint.'}), flush=True)
                time.sleep(max(interval, 15))
    finally:
        lock.rmdir()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--approved', action='store_true')
    args = parser.parse_args()
    if not args.approved:
        parser.error('Explicit approval to upload source changes is required.')
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        grant = json.loads(sys.stdin.read(16_384))
        run(Path(args.workspace).absolute(), grant)
    except KeyboardInterrupt:
        pass
    except Exception:
        # No raw exception, request, token, source content, or secret enters logs.
        print(json.dumps({'status': 'needs_attention', 'message': 'Sync stopped. Changes remain local. Check workspace, access, exclusions and checkpoint status.'}), flush=True)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
