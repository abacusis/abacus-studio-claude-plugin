import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import code_map as module
import studio_git


class Git:
    def __init__(self, names): self.names = names
    def run(self, *args):
        return subprocess.CompletedProcess(args, 0, ('\0'.join(self.names) + '\0').encode())


class CodeMapTests(unittest.TestCase):
    def test_helper_rechecks_workspace_and_does_not_install_on_query(self):
        from unittest.mock import Mock
        git = Mock()
        arguments = ['studio_git.py', 'code-map', '--project-id', '11111111-1111-4111-8111-111111111111', '--workspace', '/selected', '--query', 'billing']
        with patch.object(sys, 'argv', arguments), patch.object(studio_git, 'ensure_helper_runtime'), patch.object(studio_git, 'workspace', return_value=(Path('/selected'), {'code_map_enabled': True}, git)) as access, patch.object(studio_git, 'code_map', return_value={'status': 'ready'}) as mapping, patch.object(sys, 'stdout', StringIO()):
            self.assertEqual(studio_git.main(), 0)
        access.assert_called_once_with('/selected', '11111111-1111-4111-8111-111111111111')
        mapping.assert_called_once_with(Path('/selected'), {'code_map_enabled': True}, git, query='billing', install=False)
        git.close.assert_called_once()

    def test_helper_cannot_map_an_unauthorized_workspace(self):
        arguments = ['studio_git.py', 'code-map', '--project-id', '11111111-1111-4111-8111-111111111111', '--workspace', '/other']
        with patch.object(sys, 'argv', arguments), patch.object(studio_git, 'ensure_helper_runtime'), patch.object(studio_git, 'workspace', side_effect=ValueError('Unauthorized workspace')), patch.object(studio_git, 'code_map') as mapping, patch.object(sys, 'stderr', StringIO()):
            self.assertEqual(studio_git.main(), 1)
        mapping.assert_not_called()

    @unittest.skipUnless(os.environ.get('GRAPHIFY_TEST_PYTHON'), 'Optional real Graphify runtime smoke test')
    def test_real_graphify_maps_local_typescript_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'billing.ts').write_text('export function billing() { return 42; }')
            (root / 'app.ts').write_text("import { billing } from './billing'; export function orders() { return billing(); }")
            with patch.object(module, 'runtime', return_value=Path(os.environ['GRAPHIFY_TEST_PYTHON'])):
                result = module.code_map(root, {'code_map_enabled': True}, Git(['app.ts', 'billing.ts']), 'billing')
            self.assertEqual(result['status'], 'ready', result)
            self.assertTrue(result['matches'])
            self.assertTrue(result['relationships'])
    def test_disabled_never_installs_or_reads_source(self):
        with patch.object(module, 'runtime') as runtime:
            self.assertEqual(module.code_map('.', {}, None), {'status': 'disabled'})
            runtime.assert_not_called()

    def test_snapshot_excludes_hidden_dependencies_secrets_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            names = ['src/app.ts', '.env', '.aws/key.py', 'node_modules/x.js', 'src/secrets.ts', 'dist/app.js', '../outside.py']
            for name in names[:-1]:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('content')
            (root / 'link.py').symlink_to(root / 'src/app.ts')
            self.assertEqual(list(module.sources(root, Git(names + ['link.py']))), ['src/app.ts'])

    def test_caps_fail_instead_of_silently_mapping_partial_project(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'app.py').write_text('12345')
            with patch.object(module, 'MAX_FILE', 4):
                with self.assertRaises(ValueError): module.sources(root, Git(['app.py']))

    def test_refresh_hashes_content_and_detects_deletions(self):
        self.assertNotEqual(module.fingerprint({'app.py': b'a'}), module.fingerprint({'app.py': b'b'}))
        self.assertNotEqual(module.fingerprint({'app.py': b'a'}), module.fingerprint({}))

    def test_ready_query_then_changed_file_rebuilds(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'app.py').write_text('def billing(): pass')
            calls = []
            def extract(argv, **kwargs):
                snapshot = Path(argv[-1])
                self.assertEqual([p.name for p in snapshot.iterdir()], ['app.py'])
                calls.append(snapshot)
                kwargs['stdout'].write(json.dumps({'nodes': [{'id': '1', 'label': 'billing', 'source_file': 'app.py'}], 'edges': [], 'failed_sources': []}).encode())
                return subprocess.CompletedProcess(argv, 0)
            with patch.object(module, 'runtime', return_value=Path(sys.executable)), patch.object(module.subprocess, 'run', side_effect=extract):
                first = module.code_map(root, {'code_map_enabled': True}, Git(['app.py']), 'billing')
                self.assertEqual(first['status'], 'ready')
                self.assertTrue(first['refreshed'])
                self.assertEqual(first['matches'][0]['label'], 'billing')
                second = module.code_map(root, {'code_map_enabled': True}, Git(['app.py']), 'billing')
                self.assertFalse(second['refreshed'])
                (root / 'app.py').write_text('def billing(): return 1')
                self.assertTrue(module.code_map(root, {'code_map_enabled': True}, Git(['app.py']), 'billing')['refreshed'])
            self.assertEqual(len(calls), 2)
            self.assertTrue(all(not p.exists() for p in calls))

    def test_storage_symlink_fails_open_without_writing_outside(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory).resolve()
            (root / '.studio').symlink_to(Path(outside).resolve(), target_is_directory=True)
            self.assertEqual(module.code_map(root, {'code_map_enabled': True}, None)['status'], 'unavailable')
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_runtime_failure_is_optional_and_releases_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with patch.object(module, 'runtime', side_effect=ValueError('private error')):
                result = module.code_map(root, {'code_map_enabled': True}, None)
                self.assertEqual(result['status'], 'unavailable')
                self.assertNotIn('private error', json.dumps(result))
                self.assertFalse((root / '.studio/code-map/busy').exists())


if __name__ == '__main__': unittest.main()
