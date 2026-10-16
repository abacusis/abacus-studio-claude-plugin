import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from sandbox_environment import provision

class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(['git', 'init', str(self.root)], check=True, capture_output=True)
        class Git:
            def text(_, *args):
                return subprocess.check_output(['git', '-C', str(self.root), *args]).decode().strip()
        self.git = Git()
        self.ref = 'abcdefghijklmnopqrst'
        self.config = {'sandbox_services': [{'kind': 'supabase', 'project_ref': self.ref}]}
        self.values = {'VITE_SUPABASE_URL': f'https://{self.ref}.supabase.co',
                       'VITE_SUPABASE_PROJECT_ID': self.ref, 'VITE_SUPABASE_PUBLISHABLE_KEY': 'sb_publishable_example'}
    def provision(self):
        return provision(self.root, 'project', self.config, lambda *_: {'environment': self.values}, self.git)
    def test_writes_ignored_env_without_returning_values_and_refreshes(self):
        names = self.provision()
        self.assertNotIn('sb_publishable_example', json.dumps(names))
        self.assertEqual(self.git.text('check-ignore', '.env'), '.env')
        self.assertNotIn('sb_publishable_example', (self.root / '.studio/environment.json').read_text())
        self.values['VITE_SUPABASE_PUBLISHABLE_KEY'] = 'sb_publishable_rotated'
        self.provision()
        self.assertIn('sb_publishable_rotated', (self.root / '.env').read_text())
    def test_nextjs_receives_only_requested_public_aliases(self):
        self.config['required_env_names'] = ['NEXT_PUBLIC_SUPABASE_URL', 'NEXT_PUBLIC_SUPABASE_ANON_KEY']
        self.values['SUPABASE_SECRET_KEY'] = 'sb_secret_' + 'a' * 40
        names = self.provision()
        content = (self.root / '.env').read_text()
        self.assertIn('NEXT_PUBLIC_SUPABASE_URL', names)
        self.assertIn('NEXT_PUBLIC_SUPABASE_ANON_KEY="sb_publishable_example"', content)
        self.assertNotIn('NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY', content)
        self.assertNotIn('NEXT_PUBLIC_SUPABASE_SECRET', content)
    def test_nextjs_alias_conflicts_preserve_existing_values(self):
        self.config['required_env_names'] = ['NEXT_PUBLIC_SUPABASE_URL']
        path = self.root / '.env'
        path.write_text('NEXT_PUBLIC_SUPABASE_URL=existing\n')
        with self.assertRaises(ValueError):
            self.provision()
        self.assertEqual(path.read_text(), 'NEXT_PUBLIC_SUPABASE_URL=existing\n')
    def test_server_secret_is_private_ignored_and_rotated_without_metadata_leak(self):
        secret = 'sb_secret_' + 'a' * 40
        self.values['SUPABASE_SECRET_KEY'] = secret
        names = self.provision()
        self.assertNotIn(secret, json.dumps(names))
        self.assertNotIn(secret, (self.root / '.studio/environment.json').read_text())
        self.assertEqual((self.root / '.env').stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.git.text('check-ignore', '.env'), '.env')
        from sync_workspace import SECRET
        self.assertIsNotNone(SECRET.search(secret))
        self.values['SUPABASE_SECRET_KEY'] = 'sb_secret_' + 'b' * 40
        self.provision()
        self.assertNotIn(secret, (self.root / '.env').read_text())
        del self.values['SUPABASE_SECRET_KEY']
        self.provision()
        self.assertNotIn('SUPABASE_SECRET_KEY', (self.root / '.env').read_text())
    def test_preserves_existing_and_edited_values(self):
        path = self.root / '.env'
        path.write_text('VITE_SUPABASE_URL=existing\n')
        with self.assertRaises(ValueError): self.provision()
        self.assertEqual(path.read_text(), 'VITE_SUPABASE_URL=existing\n')
        path.unlink()
        self.provision()
        path.write_text(path.read_text().replace('sb_publishable_example', 'edited'))
        with self.assertRaises(ValueError): self.provision()
    def test_refuses_symlinks_and_unapproved_variables(self):
        (self.root / '.env').symlink_to(self.root / 'other')
        with self.assertRaises(ValueError): self.provision()
        (self.root / '.env').unlink()
        self.values['SUPABASE_SERVICE_ROLE_KEY'] = 'secret'
        with self.assertRaises(ValueError): self.provision()
    def test_refuses_tracked_env_and_wrong_project(self):
        (self.root / '.env').write_text('')
        subprocess.run(['git', '-C', str(self.root), 'add', '.env'], check=True)
        with self.assertRaises(ValueError): self.provision()
    def test_refuses_environment_overrides(self):
        (self.root / '.env.local').write_text('VITE_SUPABASE_URL=production\n')
        with self.assertRaises(ValueError): self.provision()
        self.assertFalse((self.root / '.env').exists())
        self.values['VITE_SUPABASE_PROJECT_ID'] = 'production'
        with self.assertRaises(ValueError): self.provision()

if __name__ == '__main__': unittest.main()
