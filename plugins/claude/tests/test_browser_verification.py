import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import browser_verification as browser
import studio_git


class Git:
    def __init__(self, root): self.root = root
    def run(self, *args, check=True):
        result = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True)
        if check and result.returncode: raise ValueError('Fixture Git failed')
        return result


class BrowserTests(unittest.TestCase):
    def test_only_loopback_http_without_secrets_is_accepted(self):
        for url in ['http://127.0.0.1:5173/', 'http://localhost:8080/page', 'http://[::1]:3000/']:
            self.assertTrue(browser.local_url(url))
        for url in ['https://example.com', 'http://169.254.169.254:80', 'file:///tmp/a', 'http://127.0.0.1', 'http://user:pass@localhost:80', 'http://localhost:80/?key=secret', 'http://localhost:80/#token', 'http://127.1:80', 'http://localhost:99999']:
            with self.subTest(url=url), self.assertRaises(ValueError): browser.local_url(url)

    def test_plan_rejects_scripts_unapproved_interactions_and_implicit_writes(self):
        self.assertEqual(browser.validate_plan({})['viewports'], ['desktop', 'mobile'])
        for plan in [{'script': 'code'}, {'checks': [{'criterion': 'R1', 'action': 'evaluate', 'selector': 'body'}]},
                     {'checks': [{'criterion': 'R1', 'action': 'click', 'selector': 'button'}]},
                     {'allow_writes': True}, {'viewports': ['desktop', 'mobile'], 'allow_writes': True, 'write_approval': 'Create one sandbox record'},
                     {'allowed_origins': ['https://example.com/path']}, {'allowed_origins': ['https://*.example.com']},
                     {'allowed_origins': ['https://user:pass@example.com']}, {'interactions_approved': 'true'}]:
            with self.subTest(plan=plan), self.assertRaises(ValueError): browser.validate_plan(plan)
        plan = browser.validate_plan({'viewports': ['desktop'], 'allow_writes': True, 'write_approval': 'Create one sandbox record', 'interactions_approved': True, 'checks': [{'criterion': 'R1', 'action': 'click', 'selector': '#save'}]})
        self.assertTrue(plan['allow_writes'])

    def test_capture_requires_approval_before_runtime_or_files(self):
        with patch.object(browser, 'runtime') as runtime:
            with self.assertRaises(ValueError): browser.verify(Path('/unused'), 'http://localhost:8080', {}, None)
            runtime.assert_not_called()

    def test_runtime_does_not_forward_cloud_or_app_environment(self):
        with patch.dict(os.environ, {'SUPABASE_SECRET_KEY': 'not-for-worker', 'AWS_SECRET_ACCESS_KEY': 'not-for-worker', 'PLAYWRIGHT_BROWSERS_PATH': '/untrusted'}):
            env = browser.runtime_env(Path('/approved/runtime'))
        self.assertNotIn('SUPABASE_SECRET_KEY', env)
        self.assertNotIn('AWS_SECRET_ACCESS_KEY', env)
        self.assertEqual(env['PLAYWRIGHT_BROWSERS_PATH'], '/approved/runtime/browsers')

    def test_helper_requires_authorization_and_does_not_install_on_capture(self):
        from unittest.mock import Mock
        git = Mock()
        arguments = ['studio_git.py', 'browser-verify', '--project-id', '11111111-1111-4111-8111-111111111111', '--workspace', '/approved', '--url', 'http://127.0.0.1:8080', '--approved']
        with patch.object(sys, 'argv', arguments), patch.object(sys, 'stdin', StringIO('{}')), patch.object(sys, 'stdout', StringIO()), patch.object(studio_git, 'ensure_helper_runtime'), patch.object(studio_git, 'workspace', return_value=(Path('/approved'), {}, git)) as access, patch.object(browser, 'verify', return_value={'status': 'captured'}) as capture, patch.object(browser, 'runtime') as install:
            self.assertEqual(studio_git.main(), 0)
        access.assert_called_once()
        capture.assert_called_once_with(Path('/approved'), 'http://127.0.0.1:8080', {}, git, approved=True, sandbox_services=[])
        install.assert_not_called()
        git.close.assert_called_once()
        with patch.object(sys, 'argv', arguments[:-1]), patch.object(sys, 'stderr', StringIO()), patch.object(studio_git, 'ensure_helper_runtime'), patch.object(studio_git, 'workspace') as access:
            self.assertEqual(studio_git.main(), 1)
            access.assert_not_called()

    def test_source_fingerprint_changes_and_excludes_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'index.html').write_text('first')
            (root / '.env').write_text('private')
            git = Git(root)
            first = browser.source_state(root, git)
            (root / '.env').write_text('different private')
            self.assertEqual(first, browser.source_state(root, git))
            (root / 'index.html').write_text('second')
            self.assertNotEqual(first, browser.source_state(root, git))

    def test_changed_source_marks_captured_result_stale(self):
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            git = Mock()
            git.run.return_value = subprocess.CompletedProcess([], 0, b'')
            worker = subprocess.CompletedProcess([], 0, json.dumps({'status': 'captured', 'screenshots': []}), '')
            with patch.object(browser, 'source_state', side_effect=['before', 'after']), patch.object(browser, 'runtime', return_value=(Path(sys.executable), root)), patch.object(browser.subprocess, 'run', return_value=worker):
                result = browser.verify(root, 'http://127.0.0.1:8080', {}, git, approved=True)
            self.assertEqual(result['status'], 'stale')
            self.assertFalse(result['independent_verification'])
            self.assertEqual(result['image_inspection'], 'not_performed_by_helper')
            self.assertTrue(Path(result['evidence_file']).is_file())

    def test_supabase_resource_must_match_configured_sandbox(self):
        with patch.object(browser, 'runtime') as runtime:
            with self.assertRaisesRegex(ValueError, 'configured sandbox'):
                browser.verify(Path('/unused'), 'http://127.0.0.1:8080', {'allowed_origins': ['https://other-project.supabase.co']}, None, approved=True,
                               sandbox_services=[{'kind': 'supabase', 'project_ref': 'configured-sandbox'}])
            runtime.assert_not_called()


@unittest.skipUnless(os.environ.get('ABACUS_BROWSER_TEST_HOME'), 'Optional installed Playwright/Chromium smoke tests')
class LiveBrowserTests(unittest.TestCase):
    def test_real_capture_assertions_interaction_and_blocked_post(self):
        counts = {'posts': 0}
        html = b'''<!doctype html><html><head><meta charset="utf-8"><title>Fixture</title><style>body{font:20px sans-serif;margin:24px}button{padding:12px}main{max-width:800px}</style></head><body><main><h1>Invoice overview</h1><button id="show" onclick="document.getElementById('state').textContent='Details shown'">Show details</button><p id="state">Ready</p><button id="save" onclick="fetch('/save',{method:'POST'}).catch(()=>{})">Save</button></main></body></html>'''
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200); self.send_header('Content-Type', 'text/html'); self.end_headers(); self.wfile.write(html)
            def do_POST(self):
                counts['posts'] += 1
                self.send_response(200); self.end_headers()
            def log_message(self, *_): pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory, patch.object(Path, 'home', return_value=Path(os.environ['ABACUS_BROWSER_TEST_HOME'])):
                root = Path(directory).resolve()
                subprocess.run(['git', 'init', '-q', str(root)], check=True)
                (root / '.git/info/exclude').write_text('/.studio/\n')
                (root / 'index.html').write_bytes(html)
                url = f'http://127.0.0.1:{server.server_port}/'
                plan = {'interactions_approved': True, 'checks': [
                    {'criterion': 'R1', 'action': 'text', 'selector': 'h1', 'text': 'Invoice overview'},
                    {'criterion': 'R2', 'action': 'click', 'selector': '#show'},
                    {'criterion': 'R2', 'action': 'text', 'selector': '#state', 'text': 'Details shown'}]}
                result = browser.verify(root, url, plan, Git(root), approved=True)
                self.assertEqual(result['status'], 'captured', result)
                self.assertEqual(len(result['screenshots']), 2)
                self.assertEqual(len(result['checks']), 6)
                self.assertEqual(result['image_inspection'], 'not_performed_by_helper')
                for item in result['screenshots']:
                    self.assertEqual(Path(item['path']).read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
                if os.environ.get('ABACUS_BROWSER_KEEP_EVIDENCE'):
                    import shutil
                    shutil.copytree(Path(result['evidence_file']).parent, Path(os.environ['ABACUS_BROWSER_KEEP_EVIDENCE']) / 'capture')
                failed = browser.verify(root, url, {'checks': [{'criterion': 'R3', 'action': 'text', 'selector': 'h1', 'text': 'This must fail'}]}, Git(root), approved=True)
                self.assertEqual(failed['status'], 'failed')
                blocked = browser.verify(root, url, {'viewports': ['desktop'], 'interactions_approved': True, 'checks': [
                    {'criterion': 'R4', 'action': 'click', 'selector': '#save'},
                    {'criterion': 'R4', 'action': 'text', 'selector': '#state', 'text': 'Ready'}]}, Git(root), approved=True)
                self.assertEqual(blocked['status'], 'failed', blocked)
                self.assertGreater(blocked['blocked']['requests'], 0)
                self.assertEqual(counts['posts'], 0)
        finally: server.shutdown(); server.server_close(); thread.join(timeout=5)


if __name__ == '__main__': unittest.main()
