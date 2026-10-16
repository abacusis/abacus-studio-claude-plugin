import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('download', Path(__file__).parents[1] / 'scripts/download_workspace.py')
download = importlib.util.module_from_spec(spec)
spec.loader.exec_module(download)

class DownloadTest(unittest.TestCase):
    def test_extract_and_preserve_existing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / 'archive.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('app-abc/package.json', '{"scripts":{}}')
                z.writestr('app-abc/src/app.txt', 'app')
            target = root / 'workspace'
            download.extract_workspace(archive, {'source_commit': 'a'*40, 'download_url': 'private-link'}, target)
            self.assertEqual((target/'src/app.txt').read_text(), 'app')
            metadata = json.loads((target/'.studio/workspace.json').read_text())
            self.assertEqual(metadata['source_commit'], 'a'*40)
            self.assertNotIn('download_url', metadata)
            self.assertEqual(len(metadata['baseline_file_sha256']), 2)
            with self.assertRaises(ValueError):
                download.extract_workspace(archive, {}, target)

    def test_unsafe_paths_links_and_metadata(self):
        for name in ['app/../../outside', '/absolute', 'app/.git/config', 'app/.studio/workspace.json', 'app/.gitmodules', 'app/a\\b']:
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with zipfile.ZipFile(root/'source.zip', 'w') as z:
                    z.writestr(name, 'unsafe')
                with self.assertRaises(ValueError):
                    download.extract_workspace(root/'source.zip', {}, root/'workspace')
                self.assertFalse((root/'workspace').exists())
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)/'symlink.zip'
            with zipfile.ZipFile(path, 'w') as z:
                entry = zipfile.ZipInfo('app/link')
                entry.external_attr = 0o120777 << 16
                z.writestr(entry, '../outside')
            with zipfile.ZipFile(path) as z, self.assertRaises(ValueError):
                download.archive_entries(z)

    def test_manifest_validation(self):
        sha = 'a'*40
        value = {'schema_version': 1, 'archive_format': 'zip', 'repository': 'example/app', 'source_commit': sha,
                 'download_url': f'https://codeload.github.com/example/app/legacy.zip/{sha}?token=temporary', 'expires_at': '2099-01-01T00:00:00Z'}
        download.validate_manifest(value)
        for update in [{'download_url': 'https://evil.test/source.zip'}, {'source_commit': 'not-a-sha'}, {'expires_at': '2000-01-01T00:00:00Z'}]:
            with self.assertRaises(ValueError):
                download.validate_manifest({**value, **update})

if __name__ == '__main__':
    unittest.main()
