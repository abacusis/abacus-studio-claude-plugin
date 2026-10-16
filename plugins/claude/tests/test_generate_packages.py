import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import generate_packages as generated


class GenerationTests(unittest.TestCase):
    def test_generate_both_and_check_idempotent_then_detect_source_change(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            wanted = {'claude': {'skills/x/SKILL.md': b'Claude'}, 'codex': {'skills/x/SKILL.md': b'Codex'}}
            with patch.object(generated, 'expected', return_value=wanted):
                self.assertEqual(generated.sync(root)['status'], 'generated')
                self.assertEqual(generated.sync(root, check=True)['status'], 'current')
                before = (root / 'plugins/claude/skills/x/SKILL.md').stat().st_mtime_ns
                generated.sync(root)
                self.assertEqual(before, (root / 'plugins/claude/skills/x/SKILL.md').stat().st_mtime_ns)
                wanted['codex']['skills/x/SKILL.md'] = b'new'
                with self.assertRaises(ValueError): generated.sync(root, check=True)
                generated.sync(root)
                self.assertEqual((root / 'plugins/codex/skills/x/SKILL.md').read_bytes(), b'new')

    def test_local_edit_in_one_target_preserves_both(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            wanted = {'claude': {'file.md': b'old'}, 'codex': {'file.md': b'old'}}
            with patch.object(generated, 'expected', return_value=wanted):
                generated.sync(root)
                (root / 'plugins/codex/file.md').write_bytes(b'user edit')
                wanted['claude']['file.md'] = b'new'
                with self.assertRaises(ValueError): generated.sync(root)
                self.assertEqual((root / 'plugins/claude/file.md').read_bytes(), b'old')
                self.assertEqual((root / 'plugins/codex/file.md').read_bytes(), b'user edit')

    def test_unowned_directory_and_symlink_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / 'plugins/codex'
            folder.mkdir(parents=True)
            (folder / 'user.md').write_bytes(b'keep')
            wanted = {'claude': {'file.md': b'new'}, 'codex': {'file.md': b'new'}}
            with patch.object(generated, 'expected', return_value=wanted):
                with self.assertRaises(ValueError): generated.sync(root)
                self.assertFalse((root / 'plugins/claude').exists())
                self.assertEqual((folder / 'user.md').read_bytes(), b'keep')
            with self.assertRaises(ValueError): generated.safe_name('../escape')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'plugins').symlink_to(root / 'outside')
            with patch.object(generated, 'expected', return_value=wanted):
                with self.assertRaises(ValueError): generated.sync(root)

    def test_catalogs_select_matching_folders_and_standalone_claude_selects_root(self):
        import build_release
        claude = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        codex = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(claude['plugins'][0]['source'], './plugins/claude')
        self.assertEqual(codex['plugins'][0]['source']['path'], './plugins/codex')
        rendered = build_release.render_target(ROOT, 'claude')
        self.assertEqual(json.loads(rendered['.claude-plugin/marketplace.json'])['plugins'][0]['source'], './')
        self.assertFalse(any(name.startswith('plugins/') for name in rendered))
