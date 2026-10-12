import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from install_skills import install

class SkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sha = 'a' * 40
    def config(self, extra=None):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            base = f'example-{self.sha}/'
            archive.writestr(base + 'LICENSE', 'Example license')
            archive.writestr(base + 'plugin/skills/design/SKILL.md', '---\nname: design\n---\nInstructions')
            archive.writestr(base + 'plugin/skills/design/reference/test.md', 'Reference')
            archive.writestr(base + '.claude/settings.json', 'DO NOT INSTALL HOOKS')
            if extra:
                archive.writestr(base + 'plugin/skills/design/' + extra, 'unsafe')
        data = buffer.getvalue()
        package = {'id': 'design', 'repository': 'example/example', 'commit': self.sha,
                   'sha256': hashlib.sha256(data).hexdigest(), 'path': 'plugin/skills/design', 'hooks': False}
        return {'skill_packages': [package]}, data
    def test_installs_only_skill_payload_and_license_without_hooks(self):
        config, data = self.config()
        result = install(self.root, config, lambda _: data)
        self.assertEqual(result[0]['state'], 'installed')
        self.assertTrue((self.root / '.claude/skills/design/LICENSE').exists())
        self.assertFalse((self.root / '.claude/settings.json').exists())
        self.assertEqual(install(self.root, config, lambda _: self.fail('must not redownload'))[0]['state'], 'already_installed')
    def test_existing_and_edited_skills_are_preserved(self):
        config, data = self.config()
        install(self.root, config, lambda _: data)
        path = self.root / '.claude/skills/design/SKILL.md'
        path.write_text('user changes')
        with self.assertRaises(ValueError): install(self.root, config, lambda _: data)
        self.assertEqual(path.read_text(), 'user changes')
    def test_checksum_and_traversal_fail_before_install(self):
        config, data = self.config()
        with self.assertRaises(ValueError): install(self.root, config, lambda _: data + b'changed')
        config, data = self.config('../../outside')
        with self.assertRaises(ValueError): install(self.root, config, lambda _: data)
        self.assertFalse((self.root / '.claude/skills/design').exists())
    def test_symlink_and_unpinned_source_refused(self):
        config, data = self.config()
        config['skill_packages'][0]['commit'] = 'main'
        with self.assertRaises(ValueError): install(self.root, config, lambda _: data)
        config, data = self.config()
        (self.root / '.claude').symlink_to(self.root / 'elsewhere')
        with self.assertRaises(ValueError): install(self.root, config, lambda _: data)
