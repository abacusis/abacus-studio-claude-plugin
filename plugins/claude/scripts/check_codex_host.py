"""No-inference Codex host smoke test in a disposable CODEX_HOME; no hook trust."""
import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import tempfile
import time
from build_release import build
from codex_agents import install


def check(root):
    with tempfile.TemporaryDirectory(prefix='abacus-codex-host-') as temp:
        folder = Path(temp)
        package = Path(build(root, folder / 'package', 'codex')['folder'])
        home, app = folder / 'home', folder / 'app'
        home.mkdir()
        app.mkdir()
        subprocess.run(['git', 'init', '-q', str(app)], check=True)
        (app / '.studio').mkdir()
        profiles = install(app, True, package)['profiles']
        env = {**os.environ, 'CODEX_HOME': str(home)}
        for args in (['marketplace', 'add', str(package)], ['add', 'abacus-studio@abacus-studio-codex']):
            result = subprocess.run(['codex', 'plugin', *args], env=env, cwd=app,
                                    capture_output=True, text=True, timeout=30)
            if result.returncode:
                raise ValueError('Isolated Codex plugin registration failed: ' + result.stderr[-1000:])
        process = subprocess.Popen(['codex', 'app-server', '--stdio'], env=env, cwd=app,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, text=True, bufsize=1)
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        def send(value):
            process.stdin.write(json.dumps(value) + '\n')
            process.stdin.flush()
        try:
            send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name':'abacus-smoke','version':'1'}, 'capabilities': {'experimentalApi': True}}})
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if not selector.select(1):
                    continue
                line = process.stdout.readline()
                if not line:
                    raise ValueError('Codex app-server closed before discovery.')
                response = json.loads(line)
                if response.get('id') == 1:
                    if 'error' in response:
                        raise ValueError('Codex initialization failed.')
                    send({'method':'initialized'})
                    send({'id':2,'method':'skills/list','params':{'cwds':[str(app)],'forceReload':True}})
                elif response.get('id') == 2:
                    if 'error' in response:
                        raise ValueError('Codex skill discovery failed.')
                    entries = response['result'].get('data', [])
                    errors = [error for entry in entries for error in entry.get('errors', [])]
                    names = {skill['name'] for entry in entries for skill in entry.get('skills', []) if skill['name'].startswith('abacus-')}
                    if errors or len(names) != 11:
                        raise ValueError('Codex did not discover all eleven Abacus skills without errors.')
                    return {'codex_version': subprocess.check_output(['codex','--version'], env=env, text=True).strip(),
                            'skills_discovered': sorted(names), 'project_profiles_written': profiles,
                            'native_agent_execution_tested': False, 'model_inference_performed': False,
                            'hook_trust_changed': False, 'normal_installation_changed': False}
            raise ValueError('Codex skill discovery timed out.')
        finally:
            selector.close()
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == '__main__':
    try:
        print(json.dumps(check(Path(__file__).resolve().parents[1]), indent=2))
    except Exception as error:
        sys.exit(str(error))
