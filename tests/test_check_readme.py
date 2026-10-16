import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('readme_check', Path(__file__).parents[1] / 'scripts/check_readme.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ReadmeTests(unittest.TestCase):
    def fixture(self, root):
        (root / '.claude-plugin').mkdir()
        (root / 'agents').mkdir()
        (root / '.claude-plugin/plugin.json').write_text(json.dumps({'version': '1.2.3'}))
        (root / 'agents/example.md').write_text('# Abacus Example Reviewer\n')
        (root / 'README.md').write_text("### What's new in 1.2.3\nExample Reviewer helps check changes.\n")

    def test_version_and_specialist_coverage(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            self.assertEqual(checker.validate(root), '1.2.3')
            (root / 'README.md').write_text("### What's new in 0.0.1\nExample Reviewer\n")
            with self.assertRaisesRegex(ValueError, 'version'):
                checker.validate(root)
            (root / 'README.md').write_text("### What's new in 1.2.3\n")
            with self.assertRaisesRegex(ValueError, 'specialist'):
                checker.validate(root)

    def test_git_change_requires_readme_update(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            git('init')
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'Fixture')
            base = git('rev-parse', 'HEAD')
            (root / 'agents/example.md').write_text('# Abacus Example Reviewer\nUpdated instructions.\n')
            with self.assertRaisesRegex(ValueError, 'Every change set'):
                checker.validate(root, base)
            with (root / 'README.md').open('a') as readme:
                readme.write('Maintenance: clearer review instructions.\n')
            self.assertEqual(checker.validate(root, base), '1.2.3')
            with self.assertRaisesRegex(ValueError, 'SHA'):
                checker.validate(root, '--bad-ref')
            self.assertEqual(checker.validate(root, '0' * 40), '1.2.3')
