import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import studio_git as module


class LocalGit:
    def __init__(self, root):
        self.root = root
        self.calls = []
        self.fail_fetch = False
    def run(self, *args, check=True, input=None):
        self.calls.append(args)
        if self.fail_fetch and args[0] == 'fetch':
            raise ValueError('Offline')
        result = subprocess.run(['git', '-C', str(self.root), *args], input=input, capture_output=True)
        if check and result.returncode:
            raise ValueError('Git failed')
        return result
    def text(self, *args):
        return self.run(*args).stdout.decode().strip()
    def close(self):
        pass


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.seed, self.remote, self.root = [self.base / name for name in ('seed', 'remote.git', 'client')]
        self.seed.mkdir()
        self.command('init', '-b', 'sandbox', root=self.seed)
        self.identity(self.seed)
        (self.seed / 'app.txt').write_text('Original title\n')
        self.command('add', '.', root=self.seed)
        self.command('commit', '-m', 'Initial', root=self.seed)
        self.command('clone', '--bare', str(self.seed), str(self.remote), root=self.base)
        self.command('clone', str(self.remote), str(self.root), root=self.base)
        self.identity(self.root)
        (self.root / '.studio').mkdir()
        with (self.root / '.git/info/exclude').open('a') as output:
            output.write('\n/.studio/\n')
        self.git = LocalGit(self.root)
        self.config = {'repository': 'example/client', 'base_branch': 'sandbox',
                       'commands': {'test': None, 'build': None}}
        self.patch_workspace = patch.object(module, 'workspace', return_value=(self.root, self.config, self.git))
        self.patch_workspace.start()
        self.addCleanup(self.patch_workspace.stop)
        self.patch_record = patch.object(module, 'operation', return_value={'status': 'recorded'})
        self.patch_record.start()
        self.addCleanup(self.patch_record.stop)
    def command(self, *args, root):
        return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True).stdout.decode().strip()
    def identity(self, root):
        self.command('config', 'user.name', 'Test', root=root)
        self.command('config', 'user.email', 'test@example.com', root=root)
    def run_action(self, action, **kwargs):
        return module.execute(action, self.root, 'test-app', **kwargs)
    def remote_edit(self):
        self.command('remote', 'add', 'origin', str(self.remote), root=self.seed)
        (self.seed / 'app.txt').write_text('Team title\n')
        self.command('add', '.', root=self.seed)
        self.command('commit', '-m', 'Team update', root=self.seed)
        self.command('push', 'origin', 'sandbox', root=self.seed)

    def test_fetch_failure_never_stages_or_commits(self):
        (self.root / 'app.txt').write_text('Client title\n')
        before = self.git.text('rev-parse', 'HEAD')
        self.git.calls.clear()
        self.git.fail_fetch = True
        with self.assertRaises(ValueError):
            self.run_action('prepare', description='Update title', approved=True)
        self.assertEqual(self.git.calls[0][0], 'fetch')
        self.assertFalse(any(call[0] in ('add', 'commit', 'merge') for call in self.git.calls))
        self.assertEqual(self.git.text('rev-parse', 'HEAD'), before)
        self.assertEqual((self.root / 'app.txt').read_text(), 'Client title\n')

    def test_conflicts_pause_and_cancel_preserves_client_commit(self):
        self.remote_edit()
        (self.root / 'app.txt').write_text('Client title\n')
        result = self.run_action('prepare', description='Update title', approved=True)
        self.assertEqual(result['status'], 'conflicts')
        self.assertEqual(result['conflicts'], ['app.txt'])
        with self.assertRaises(ValueError):
            self.run_action('resolve', approved=True)
        self.run_action('cancel', approved=True)
        self.assertEqual(self.git.text('rev-parse', 'HEAD'), result['saved_commit'])
        self.assertEqual((self.root / 'app.txt').read_text(), 'Client title\n')

    def test_remote_changes_block_push_after_review(self):
        (self.root / 'app.txt').write_text('Client title\n')
        self.run_action('prepare', description='Update title', approved=True)
        self.run_action('check', approved=True)
        self.remote_edit()
        result = self.run_action('submit', approved=True)
        self.assertEqual(result['status'], 'remote_changed')
        self.assertFalse(any(call[0] == 'push' for call in self.git.calls))

    def test_submit_requires_checks_and_verifies_pushed_commit(self):
        (self.root / 'app.txt').write_text('Client title\n')
        self.run_action('prepare', description='Update title', approved=True)
        with self.assertRaises(ValueError):
            self.run_action('submit', approved=True)
        self.run_action('check', approved=True)
        result = self.run_action('submit', approved=True)
        self.assertEqual(result['commit'], self.command('rev-parse', 'sandbox', root=self.remote))

    def test_secret_files_block_before_commit(self):
        (self.root / '.env').write_text('TOKEN=example\n')
        before = self.git.text('rev-parse', 'HEAD')
        with self.assertRaises(ValueError):
            self.run_action('prepare', description='Update config', approved=True)
        self.assertEqual(self.git.text('rev-parse', 'HEAD'), before)


if __name__ == '__main__':
    unittest.main()
