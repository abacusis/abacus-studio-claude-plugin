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
        self.assertIn('agents/spec-writer.md', names)
        self.assertIn('agents/builder.md', names)
        self.assertIn('agents/verifier.md', names)
        self.assertIn('agents/code-reviewer.md', names)
        self.assertIn('scripts/browser_verification.py', names)
        self.assertIn('references/engineering/browser-verification.md', names)
        self.assertIn('hooks/hooks.json', names)
        self.assertIn('scripts/route_development.py', names)
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
                self.assertIn('LICENSE', archive.namelist())
                self.assertIn('THIRD_PARTY_NOTICES.md', archive.namelist())
                self.assertIn('skills/engineering/SKILL.md', archive.namelist())
                self.assertIn('agents/spec-writer.md', archive.namelist())
                self.assertIn('agents/builder.md', archive.namelist())
                self.assertIn('agents/verifier.md', archive.namelist())
                self.assertIn('agents/code-reviewer.md', archive.namelist())
                self.assertIn('hooks/hooks.json', archive.namelist())
                self.assertIn('skills/security/SKILL.md', archive.namelist())
                self.assertIn('skills/project-knowledge/SKILL.md', archive.namelist())
                self.assertIn('references/security/review.md', archive.namelist())
                self.assertIn('references/security/upstream.md', archive.namelist())
                for name in ('planning', 'testing', 'debugging', 'architecture', 'review', 'upstream', 'specification', 'spec-kit-upstream'):
                    self.assertIn('references/engineering/' + name + '.md', archive.namelist())
                self.assertNotIn('.claude/settings.local.json', archive.namelist())
            with self.assertRaises(ValueError):
                release.build(Path(__file__).parents[1], output)

if __name__ == '__main__':
    unittest.main()
