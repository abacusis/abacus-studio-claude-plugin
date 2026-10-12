import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('release', Path(__file__).parents[1] / 'scripts/build_release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)

class ReleaseTests(unittest.TestCase):
    def test_distribution_excludes_local_files(self):
        names = {p.relative_to(Path(__file__).parents[1]).as_posix() for p in release.release_files(Path(__file__).parents[1])}
        self.assertIn('.claude-plugin/marketplace.json', names)
        self.assertNotIn('.claude/settings.local.json', names)
        self.assertFalse(any('__pycache__' in name or name.endswith('.pyc') for name in names))

    def test_concrete_secrets_are_detected_without_matching_regex_source(self):
        for prefix in ('sbp_', 'sb_secret_', 'ghp_'):
            self.assertIsNotNone(release.CONCRETE_SECRET.search(prefix + 'a' * 40))
        self.assertIsNone(release.CONCRETE_SECRET.search("'sbp_' + 'a' * 40"))

    def test_package_round_trip_and_no_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'public'
            result = release.build(Path(__file__).parents[1], output)
            with zipfile.ZipFile(result['zip']) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('RELEASE-MANIFEST.json', archive.namelist())
                self.assertNotIn('.claude/settings.local.json', archive.namelist())
            with self.assertRaises(ValueError):
                release.build(Path(__file__).parents[1], output)

if __name__ == '__main__':
    unittest.main()
