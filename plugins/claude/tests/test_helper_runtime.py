from pathlib import Path
import sys
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import helper_runtime as module


class HelperRuntimeTests(unittest.TestCase):
    def test_uses_current_interpreter_when_keyring_is_present(self):
        with patch.object(module.importlib.util, 'find_spec', return_value=object()), \
                patch.object(module.subprocess, 'run') as probe:
            self.assertEqual(module.find_helper_python(), Path(sys.executable))
        probe.assert_not_called()

    def test_finds_mac_linux_and_windows_private_venvs(self):
        for layout in ('bin/python3', 'Scripts/python.exe'):
            with self.subTest(layout=layout), \
                    patch.object(module.importlib.util, 'find_spec', return_value=None), \
                    patch.object(module.Path, 'home', return_value=Path('/client')), \
                    patch.object(module.Path, 'is_file', lambda p: str(p).endswith(layout)), \
                    patch.object(module.subprocess, 'run', return_value=Mock(returncode=0)):
                self.assertEqual(module.find_helper_python(), Path('/client/.abacus-studio/venv') / layout)

    def test_missing_environment_reports_repair_without_installing(self):
        with patch.object(module.importlib.util, 'find_spec', return_value=None), \
                patch.object(module.Path, 'is_file', return_value=False):
            with self.assertRaisesRegex(ValueError, 'missing or incomplete'):
                module.find_helper_python()

    def test_reexec_preserves_arguments_and_venv_symlink_path(self):
        interpreter = Path('/client/.abacus-studio/venv/bin/python3')
        args = ['disconnect', '--project-id', 'app-id']
        with patch.object(module, 'find_helper_python', return_value=interpreter), \
                patch.object(module.os, 'execv') as execute:
            module.ensure_helper_runtime('/plugin/studio_git.py', args)
        execute.assert_called_once_with(str(interpreter), [str(interpreter), '/plugin/studio_git.py', *args])
