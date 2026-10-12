import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('clone_workspace', Path(__file__).parents[1] / 'scripts/clone_workspace.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CloneTests(unittest.TestCase):
    def manifest(self):
        return dict(schema_version=1, source_type='git_clone', repository='example/client',
                    project_id='app-id', base_branch='sandbox', source_commit='a' * 40)

    def test_rejects_snapshot_and_credentials(self):
        for update in ({'source_type': 'github_archive'}, {'token': 'secret'},
                       {'repository': 'https://bad.example/repo'}, {'base_branch': '../main'}):
            with self.assertRaises(ValueError):
                module.validate(self.manifest() | update)

    def test_existing_destination_is_never_touched(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                module.clone(self.manifest(), root, run=lambda *a, **k: self.fail('Git invoked'))

    def test_new_clone_pins_revision_and_has_clean_remote(self):
        calls = []
        def run(args, **kwargs):
            calls.append(args)
            if 'clone' in args:
                Path(args[-1]).mkdir()
            return type('Result', (), dict(returncode=0, stdout='' if 'ls-files' in args else 'a' * 40 + '\n'))()
        with tempfile.TemporaryDirectory() as root:
            destination = Path(root) / 'client'
            self.assertEqual(module.clone(self.manifest(), destination, run)['status'], 'cloned')
            self.assertIn('https://github.com/example/client.git', calls[0])
            self.assertNotIn('--depth', calls[0])
            self.assertTrue((destination / '.studio/workspace.json').exists())


if __name__ == '__main__':
    unittest.main()
