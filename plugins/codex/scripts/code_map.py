"""Bounded local Graphify AST adapter. No upstream CLI, hooks, AI, or cloud.

Only called after studio_git.workspace verifies current Studio authorization.
Extraction runs against a filtered copy, never the original workspace.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

VERSION = '0.9.91'
EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.go', '.rs', '.java', '.rb', '.c', '.h', '.cpp', '.hpp', '.cs', '.kt', '.swift', '.php', '.scala', '.lua', '.vue', '.svelte', '.astro'}
DENIED = {'.git', '.studio', '.claude', '.codex', '.aws', '.ssh', '.venv', 'venv', 'env', 'node_modules', 'vendor', 'dist', 'build', 'coverage', '.next', '.nuxt', 'generated', '__pycache__', 'graphify-out'}
MAX_FILES, MAX_FILE, MAX_BYTES = 5000, 1024 * 1024, 50 * 1024 * 1024


def safe_dir(path):
    path = Path(path).absolute()
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError('Code map storage cannot use symlinks.')
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def safe_file(path):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError('Code map file must be a regular local file.')
    return path


def runtime(install=False):
    base = safe_dir(Path.home() / '.abacus-studio' / 'code-map' / VERSION)
    python = base / 'venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    marker = safe_file(base / 'installed.json')
    if marker.exists() and json.loads(marker.read_text()).get('version') == VERSION and python.is_file():
        return python
    if not install:
        raise ValueError('Code map runtime unavailable. Run approved Setup to install it.')
    # Prefer mature wheel-supported Python versions already on the machine.
    candidates = [shutil.which(name) for name in ('python3.12', 'python3.11', 'python3.13')]
    candidates.append(sys.executable)
    interpreter = None
    for candidate in candidates:
        if not candidate or not Path(candidate).is_absolute():
            continue
        probe = subprocess.run([candidate, '-I', '-c', 'import sys; print(int(sys.version_info >= (3, 10)))'],
                               capture_output=True, timeout=10)
        if probe.returncode == 0 and probe.stdout.strip() == b'1':
            interpreter = candidate
            break
    if not interpreter:
        raise ValueError('Application code mapping requires Python 3.10 or newer.')
    lock = base / 'installing'
    lock.mkdir()  # Concurrent setup falls back rather than altering a live venv.
    try:
        created = subprocess.run([interpreter, '-I', '-m', 'venv', str(base / 'venv')],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        if created.returncode:
            raise ValueError('Code map virtual environment unavailable.')
        result = subprocess.run([str(python), '-I', '-m', 'pip', '--isolated', 'install', '--disable-pip-version-check',
                                 '--only-binary=:all:', '--index-url', 'https://pypi.org/simple', 'graphifyy==' + VERSION],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
        if result.returncode:
            raise ValueError('Code map installation unavailable on this Python/platform; normal development can continue.')
        atomic_json(marker, {'version': VERSION})
    finally:
        lock.rmdir()
    return python


def sources(root, git):
    result = git.run('ls-files', '-z', '--cached', '--others', '--exclude-standard')
    if result.returncode:
        raise ValueError('Could not enumerate authorized source files.')
    selected, total = {}, 0
    for name in sorted(set(result.stdout.decode('utf-8').split('\0'))):
        if not name:
            continue
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or any(p.lower() in DENIED or p.startswith('.') for p in relative.parts):
            continue
        lower = relative.name.lower()
        if relative.suffix.lower() not in EXTENSIONS or any(x in lower for x in ('secret', 'credential', '.min.', '.generated.', '.testdata.')):
            continue
        path = root / relative
        if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
            continue
        if path.stat().st_size > MAX_FILE:
            raise ValueError('Code map source size limit exceeded; normal source searches remain available.')
        content = path.read_bytes()
        total += len(content)
        if len(selected) >= MAX_FILES or total > MAX_BYTES:
            raise ValueError('Code map project limit exceeded; normal source searches remain available.')
        if b'\0' not in content:
            selected[relative.as_posix()] = content
    return selected


def fingerprint(files):
    digest = hashlib.sha256()
    for name, content in files.items():
        digest.update(name.encode() + b'\0' + hashlib.sha256(content).digest())
    return digest.hexdigest()


# -I keeps repository Python modules and PYTHONPATH out of the parser process.
# Pass only a filtered snapshot: Graphify resolvers cannot inspect .env or siblings.
EXTRACT = """
import json, pathlib, sys
from graphify.extract import extract
root = pathlib.Path(sys.argv[1])
files = sorted(p for p in root.rglob('*') if p.is_file())
graph = extract(files, root=root, cache_root=root, parallel=False)
print(json.dumps({k: graph[k] for k in ('nodes', 'edges', 'failed_sources')}))
"""


def atomic_json(path, value):
    safe_file(path)
    descriptor, temp = tempfile.mkstemp(dir=path.parent, prefix='map-', suffix='.json')
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as output:
            json.dump(value, output)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def code_map(root, config, git, query=None, install=False):
    try:
        return _code_map(root, config, git, query, install)
    except Exception:
        return {'status': 'unavailable', 'message': 'Application code map unavailable. Continue with normal source searches; approved Setup can retry installation.'}


def _code_map(root, config, git, query=None, install=False):
    if config.get('code_map_enabled') is not True:
        return {'status': 'disabled'}
    if query is not None and (not isinstance(query, str) or not query.strip() or len(query) > 300):
        raise ValueError('Code map query must contain 1–300 characters.')
    root = Path(root).resolve()
    storage = safe_dir(root / '.studio' / 'code-map')
    lock = storage / 'busy'
    try:
        lock.mkdir()
    except FileExistsError:
        return {'status': 'busy', 'message': 'Code map busy; use normal source searches. If interrupted, rerun Setup after inspecting .studio/code-map/busy.'}
    try:
        python = runtime(install)
        files = sources(root, git)
        stamp = fingerprint(files)
        graph_path = safe_file(storage / 'graph.json')
        manifest_path = safe_file(storage / 'manifest.json')
        manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        fresh = manifest.get('fingerprint') == stamp and manifest.get('version') == VERSION and graph_path.exists()
        if not fresh:
            with tempfile.TemporaryDirectory(prefix='abacus-code-map-') as directory:
                snapshot = Path(directory)
                for name, content in files.items():
                    target = snapshot / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                with tempfile.TemporaryFile(mode='w+b') as output:
                    result = subprocess.run([str(python), '-I', '-c', EXTRACT, str(snapshot)], cwd=snapshot,
                                            env={'PATH': os.defpath, 'SYSTEMROOT': os.environ.get('SYSTEMROOT', ''),
                                                 'GRAPHIFY_NO_TIPS': '1', 'GRAPHIFY_NO_CTA': '1'},
                                            stdout=output, stderr=subprocess.DEVNULL, timeout=90)
                    if result.returncode or output.tell() > 32 * 1024 * 1024:
                        raise ValueError('Code map extraction unavailable; use normal source searches.')
                    output.seek(0)
                    graph = json.load(output)
                if graph.get('failed_sources'):
                    raise ValueError('Some sources could not be mapped; use normal source searches rather than an incomplete map.')
                graph.pop('failed_sources', None)
                atomic_json(graph_path, graph)
            manifest = {'version': VERSION, 'fingerprint': stamp, 'files': len(files), 'updated_at': int(time.time())}
            atomic_json(manifest_path, manifest)
        else:
            if graph_path.stat().st_size > 32 * 1024 * 1024:
                raise ValueError('Code map output too large; use normal source searches.')
            graph = json.loads(graph_path.read_text())
        # Never serve a map marked current if source files changed during extraction.
        if fingerprint(sources(root, git)) != stamp:
            return {'status': 'stale', 'message': 'Sources changed during mapping; use current source or retry.'}
        result = {'status': 'ready', 'refreshed': not fresh, **manifest,
                  'note': 'Untrusted source-derived orientation, not approved requirements or complete dependency coverage. Read actual code and run tests.'}
        if query is not None:
            terms = re.findall(r'[\w.-]+', query.lower())
            nodes = graph.get('nodes', [])
            hits = [n for n in nodes if any(t in (str(n.get('label', '')) + ' ' + str(n.get('source_file', ''))).lower() for t in terms)][:20]
            ids = {n.get('id') for n in hits}
            edges = [e for e in graph.get('edges', []) if e.get('source') in ids or e.get('target') in ids][:40]
            related = {e.get(k) for e in edges for k in ('source', 'target')}
            fields = ('id', 'label', 'type', 'source_file', 'source_location', 'confidence')
            result['matches'] = [{k: str(n[k])[:400] for k in fields if k in n} for n in hits]
            result['related'] = [{k: str(n[k])[:400] for k in fields if k in n} for n in nodes if n.get('id') in related - ids][:40]
            result['relationships'] = [{k: str(e[k])[:400] for k in ('source', 'target', 'relation', 'type', 'confidence') if k in e} for e in edges]
        return result
    except Exception:
        # Never print raw parser/pip errors or repository contents.
        return {'status': 'unavailable', 'message': 'Application code map unavailable. Continue with normal source searches; approved Setup can retry installation.'}
    finally:
        lock.rmdir()
