"""Approved local Playwright fallback; no app-controlled config or arbitrary JS.

Called by studio_git after current workspace authorization. The worker only sees
the reviewed plan and a fresh evidence directory, not keys or browser profiles.
Browser routing cannot sandbox server-side effects: verify sandbox backing first.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import uuid

if __name__ != '__main__':
    from code_map import safe_dir, atomic_json
    from sync_workspace import excluded

VERSION = '1.64.0'
VIEWPORTS = {'desktop': {'width': 1440, 'height': 900}, 'mobile': {'width': 390, 'height': 844}}


def local_url(value):
    if not isinstance(value, str) or len(value) > 2048:
        raise ValueError('Provide a bounded local preview URL.')
    try:
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme != 'http' or parsed.hostname not in ('127.0.0.1', 'localhost', '::1') or not parsed.port or parsed.username or parsed.password or parsed.query or parsed.fragment or '\\' in value or any(ord(c) < 32 for c in value):
            raise ValueError()
        return parsed, origin(value)
    except (ValueError, TypeError):
        raise ValueError('Use the verified session-owned loopback HTTP preview URL, without credentials, query, or fragment.') from None


def origin(value):
    parsed = urllib.parse.urlsplit(value)
    host = parsed.hostname or ''
    if ':' in host: host = '[' + host + ']'
    port = parsed.port
    suffix = f':{port}' if port and not ((parsed.scheme == 'http' and port == 80) or (parsed.scheme == 'https' and port == 443)) else ''
    return f'{parsed.scheme}://{host}{suffix}'


def validate_plan(value):
    allowed = {'checks', 'interactions_approved', 'allow_writes', 'write_approval', 'repeat_writes_approved', 'allowed_origins', 'viewports'}
    if not isinstance(value, dict) or set(value) - allowed:
        raise ValueError('Use a reviewed browser plan, not executable scripts.')
    for key in ('interactions_approved', 'allow_writes', 'repeat_writes_approved'):
        if key in value and type(value[key]) is not bool:
            raise ValueError('Browser approvals must be explicit booleans.')
    viewports = value.get('viewports', ['desktop', 'mobile'])
    if not isinstance(viewports, list) or not viewports or len(viewports) > 2 or any(not isinstance(v, str) or v not in VIEWPORTS for v in viewports) or len(set(viewports)) != len(viewports):
        raise ValueError('Choose desktop, mobile, or both viewports.')
    origins = value.get('allowed_origins', [])
    if not isinstance(origins, list) or len(origins) > 8:
        raise ValueError('Review up to eight exact sandbox resource origins.')
    for item in origins:
        try:
            if not isinstance(item, str): raise ValueError()
            p = urllib.parse.urlsplit(item)
            if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password or p.query or p.fragment or p.path or '*' in item or p.port == 0 or any(ord(c) < 32 for c in item) or '\\' in item:
                raise ValueError()
            if p.scheme == 'http' and p.hostname not in ('127.0.0.1', 'localhost', '::1'): raise ValueError()
        except (ValueError, TypeError):
            raise ValueError('Sandbox resource allowlist requires exact origins without paths or credentials.') from None
    if value.get('allow_writes'):
        approval = value.get('write_approval')
        if not isinstance(approval, str) or not 5 <= len(approval.strip()) <= 500:
            raise ValueError('Describe the reviewed sandbox-write approval scope.')
        if len(viewports) > 1 and value.get('repeat_writes_approved') is not True:
            raise ValueError('Repeating write flows on both viewports needs explicit approval.')
    checks = value.get('checks', [])
    if not isinstance(checks, list) or len(checks) > 12:
        raise ValueError('Use at most twelve bounded browser checks.')
    for check in checks:
        if not isinstance(check, dict) or set(check) - {'criterion', 'action', 'selector', 'text', 'value'}:
            raise ValueError('Invalid browser check.')
        if check.get('action') not in ('visible', 'text', 'click', 'fill') or not isinstance(check.get('selector'), str) or not 1 <= len(check['selector']) <= 240:
            raise ValueError('Use visible/text assertions or approved click/fill actions.')
        if not isinstance(check.get('criterion'), str) or not 1 <= len(check['criterion']) <= 100:
            raise ValueError('Link each check to a criterion.')
        if check['action'] in ('click', 'fill') and value.get('interactions_approved') is not True:
            raise ValueError('Browser interactions need approval; navigation can also affect a backend.')
        field = 'text' if check['action'] == 'text' else 'value'
        if check['action'] in ('text', 'fill') and (not isinstance(check.get(field), str) or len(check[field]) > 500):
            raise ValueError('Provide bounded expected text or non-secret input.')
    return {**value, 'viewports': viewports, 'allowed_origins': origins, 'checks': checks}


def runtime_base():
    return safe_dir(Path.home() / '.abacus-studio' / 'browser' / VERSION)


def runtime_env(base):
    # Deliberately do not forward application, cloud, or credential environment.
    env = {'PATH': os.defpath, 'HOME': str(Path.home()), 'PLAYWRIGHT_BROWSERS_PATH': str(base / 'browsers'),
           'PLAYWRIGHT_SKIP_BROWSER_GC': '1'}
    for key in ('SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'TMPDIR', 'USERPROFILE'):
        if key in os.environ: env[key] = os.environ[key]
    return env


def runtime(install=False):
    base = runtime_base()
    python = base / 'venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    marker = base / 'installed.json'
    if marker.is_symlink() or (base / 'venv').is_symlink() or (base / 'browsers').is_symlink():
        raise ValueError('Unsafe browser runtime storage.')
    if marker.is_file() and python.is_file() and json.loads(marker.read_text()).get('version') == VERSION:
        return python, base
    if not install:
        raise ValueError('Local browser runtime is not installed. Use a host browser or approved browser installation.')
    lock = base / 'installing'
    try: lock.mkdir()
    except FileExistsError: raise ValueError('A browser installation is already active or needs inspection after interruption.') from None
    try:
        candidates = [shutil.which(n) for n in ('python3.12', 'python3.11', 'python3.13')] + [sys.executable]
        interpreter = None
        for candidate in candidates:
            if not candidate or not Path(candidate).is_absolute(): continue
            probe = subprocess.run([candidate, '-I', '-c', 'import sys; print(int(sys.version_info >= (3,10)))'], capture_output=True, timeout=10)
            if probe.returncode == 0 and probe.stdout.strip() == b'1': interpreter = candidate; break
        if not interpreter: raise ValueError('Playwright requires Python 3.10 or newer.')
        commands = [[interpreter, '-I', '-m', 'venv', str(base / 'venv')],
                    [str(python), '-I', '-m', 'pip', '--isolated', 'install', '--disable-pip-version-check', '--only-binary=:all:', '--index-url', 'https://pypi.org/simple', 'playwright==' + VERSION],
                    [str(python), '-I', '-m', 'playwright', 'install', 'chromium']]
        for command in commands:
            result = subprocess.run(command, env=runtime_env(base), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
            if result.returncode: raise ValueError('Browser installation failed. Use a host browser or ask Abacus to check platform dependencies; no system packages were installed.')
        atomic_json(marker, {'version': VERSION})
        return python, base
    finally: lock.rmdir()


def source_state(root, git):
    names = git.run('ls-files', '-z', '--cached', '--others', '--exclude-standard').stdout.decode().split('\0')
    digest, total = hashlib.sha256(), 0
    for name in sorted(set(filter(None, names))):
        path = Path(name)
        if path.is_absolute() or '..' in path.parts: raise ValueError('Invalid source path.')
        if excluded(name) or any(part.startswith('.') or part.lower() in ('vendor', 'venv', 'env') or 'secret' in part.lower() or 'credential' in part.lower() for part in path.parts): continue
        source = root / path
        if any(p.is_symlink() for p in (source, *source.parents)): raise ValueError('Source symlink needs review.')
        digest.update(name.encode() + b'\0')
        if not source.exists(): digest.update(b'deleted'); continue
        if not source.is_file(): raise ValueError('Source must be a regular file.')
        with source.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                total += len(chunk)
                if total > 256 * 1024 * 1024: raise ValueError('Source fingerprint limit exceeded.')
                digest.update(chunk)
    return digest.hexdigest()


def verify(root, url, plan, git, approved=False, sandbox_services=None):
    if not approved: raise ValueError('Approve the preview target, sandbox backing, capture, and browser plan before running.')
    local_url(url)
    plan = validate_plan(plan)
    sandbox_hosts = {f"{s['project_ref']}.supabase.co" for s in (sandbox_services or []) if s.get('kind') == 'supabase' and s.get('project_ref')}
    for resource in plan['allowed_origins']:
        host = urllib.parse.urlsplit(resource).hostname
        if host and host.endswith('.supabase.co') and host not in sandbox_hosts:
            raise ValueError('Supabase resources must match Studio\'s configured sandbox project, not an arbitrary or production project.')
    root = Path(root).resolve()
    ignored = git.run('check-ignore', '--quiet', '--', '.studio/browser-evidence/probe', check=False)
    if ignored.returncode: raise ValueError('Browser evidence must be Git-ignored before capture.')
    before = source_state(root, git)
    python, base = runtime()
    storage = safe_dir(root / '.studio' / 'browser-evidence')
    output = safe_dir(storage / uuid.uuid4().hex)
    payload = {'url': url, 'plan': plan, 'output': str(output)}
    try:
        result = subprocess.run([str(python), '-I', str(Path(__file__).resolve()), '--worker'],
                                cwd=base, env=runtime_env(base), input=json.dumps(payload),
                                capture_output=True, text=True, timeout=150)
        if result.returncode: raise ValueError('Browser capture failed; no passing result is available.')
        evidence = json.loads(result.stdout)
    except (subprocess.SubprocessError, json.JSONDecodeError, OSError):
        raise ValueError('Browser capture unavailable or timed out. Existing work is preserved.') from None
    evidence.update({'runtime_version': VERSION, 'source_fingerprint': before,
                     'preview_identity': 'caller_confirmed_not_process_verified',
                     'fingerprint_scope': 'non-secret, non-generated Git-listed files including local edits; excludes environment and dependency changes',
                     'captured_at': int(time.time()), 'image_inspection': 'not_performed_by_helper',
                     'independent_verification': False})
    if source_state(root, git) != before: evidence['status'] = 'stale'
    atomic_json(output / 'result.json', evidence)
    return {**evidence, 'evidence_file': str(output / 'result.json')}


def worker(payload):
    from playwright.sync_api import sync_playwright, expect
    url, plan, output = payload['url'], payload['plan'], Path(payload['output'])
    _, target = local_url(url)
    allowed = {target, *(origin(resource) for resource in plan['allowed_origins'])}
    checks, screenshots, failures, page_errors, console_errors = [], [], [], [], []
    blocked = {'requests': 0, 'websockets': 0}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, chromium_sandbox=True)
        for viewport in plan['viewports']:
            context = browser.new_context(viewport=VIEWPORTS[viewport], service_workers='block', accept_downloads=False)
            context.route_web_socket('**/*', lambda socket: (blocked.__setitem__('websockets', blocked['websockets'] + 1), socket.close()))
            def route_request(route):
                request = route.request
                request_origin = origin(request.url)
                permitted = request_origin in allowed and (not request.is_navigation_request() or request_origin == target) and (request.method in ('GET', 'HEAD', 'OPTIONS') or plan.get('allow_writes') is True)
                if not permitted:
                    blocked['requests'] += 1
                    route.abort()
                else: route.continue_()
            context.route('**/*', route_request)
            page = context.new_page()
            page.on('pageerror', lambda _error: page_errors.append(True))
            page.on('console', lambda message: console_errors.append(True) if message.type == 'error' else None)
            page.on('dialog', lambda dialog: dialog.dismiss())
            try:
                response = page.goto(url, wait_until='domcontentloaded', timeout=20000)
                if not response or response.status >= 400: raise ValueError('Preview did not return a successful page.')
                if origin(page.url) != target: raise ValueError('Preview redirected outside the approved local origin.')
                expect(page.locator('body')).to_contain_text(__import__('re').compile(r'\S'), timeout=10000)
                for check in plan['checks']:
                    locator = page.locator(check['selector'])
                    try:
                        action = check['action']
                        if action == 'visible': expect(locator).to_be_visible(timeout=5000)
                        elif action == 'text': expect(locator).to_contain_text(check['text'], timeout=5000)
                        elif action == 'click': locator.click(timeout=5000)
                        elif action == 'fill':
                            if locator.get_attribute('type') == 'password': raise ValueError('Managed fallback does not handle password input.')
                            locator.fill(check['value'], timeout=5000)
                        checks.append({'criterion': check['criterion'], 'action': action, 'viewport': viewport, 'status': 'passed'})
                    except Exception:
                        checks.append({'criterion': check['criterion'], 'action': check['action'], 'viewport': viewport, 'status': 'failed'})
                        raise
            except Exception:
                failures.append({'viewport': viewport, 'reason': 'Navigation, rendering, or a reviewed check failed; inspect the local evidence.'})
            try:
                image = output / (viewport + '.png')
                page.screenshot(path=str(image), full_page=True, animations='disabled', timeout=10000)
                image.chmod(0o600)
                screenshots.append({'viewport': viewport, 'path': str(image)})
            except Exception: failures.append({'viewport': viewport, 'reason': 'Screenshot unavailable.'})
            context.close()
        browser.close()
    return {'status': 'failed' if failures or page_errors or console_errors or blocked['requests'] or blocked['websockets'] else 'captured',
            'checks': checks, 'screenshots': screenshots, 'failures': failures,
            'page_error_count': len(page_errors), 'console_error_count': len(console_errors), 'blocked': blocked,
            'note': 'Captured is not a visual pass. Inspect the images; browser network filtering does not isolate server-side effects or prove authorization.'}


if __name__ == '__main__':
    if sys.argv[1:] != ['--worker']: raise SystemExit('Use the authorized Studio helper.')
    try: print(json.dumps(worker(json.loads(sys.stdin.read(20000)))))
    except Exception: raise SystemExit(1)
