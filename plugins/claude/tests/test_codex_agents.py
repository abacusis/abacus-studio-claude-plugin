import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import build_release
import codex_agents


class NativeAgentsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'app'
        self.root.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / '.studio').mkdir()
        self.package = Path(build_release.build(Path(__file__).parents[1], Path(self.temp.name) / 'package', 'codex')['folder'])

    def install(self, approved=True):
        return codex_agents.install(self.root, approved, self.package)

    def test_profiles_parse_preserve_models_and_stay_local(self):
        result = self.install()
        self.assertEqual(len(result['profiles']), 8)
        for path in (self.root / '.codex/agents').glob('*.toml'):
            profile = tomllib.loads(path.read_text())
            self.assertEqual(profile['name'], path.stem)
            self.assertNotIn('model', profile)
            self.assertNotIn('sandbox_mode', profile)
            self.assertNotIn('<plugin-root>', profile['developer_instructions'])
            self.assertIn(str(self.package), profile['developer_instructions'])
            self.assertIn('Do not spawn other agents', profile['developer_instructions'])
        self.assertEqual(subprocess.check_output(['git', '-C', str(self.root), 'status', '--porcelain']).decode(), '')
        self.assertFalse((self.root / '.codex/config.toml').exists())
        self.assertEqual(self.install()['profiles'], result['profiles'])

    def test_approval_and_conflict_preflight(self):
        with self.assertRaises(ValueError):
            self.install(False)
        folder = self.root / '.codex/agents'
        folder.mkdir(parents=True)
        (folder / 'abacus-verifier.toml').write_text('user owned')
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(list(folder.iterdir()), [folder / 'abacus-verifier.toml'])
        self.assertFalse((self.root / '.studio/codex-agents.json').exists())

    def test_edited_owned_profile_not_overwritten(self):
        self.install()
        path = self.root / '.codex/agents/abacus-builder.toml'
        path.write_text('client edit')
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(path.read_text(), 'client edit')

    def test_symlink_refused(self):
        (self.root / '.codex').symlink_to(self.package, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.install()


if __name__ == '__main__':
    unittest.main()
