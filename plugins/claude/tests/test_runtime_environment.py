import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import runtime_environment as runtime


class RuntimeTests(unittest.TestCase):
    def test_requires_installed_matching_major(self):
        with patch.object(runtime.shutil, 'which', return_value='/node20/node'), patch.object(Path, 'glob', return_value=[Path('/node22/node')]), patch.object(Path, 'is_file', return_value=True), patch.object(runtime.subprocess, 'run', side_effect=[Mock(stdout='v20.20.2'), Mock(stdout='v22.23.2')]):
            env = runtime.environment({'runtime_requirements': ['node 22', 'bun']})
            self.assertTrue(env['PATH'].startswith('/node22' + os.pathsep))

    def test_missing_runtime_stops_instead_of_falling_back(self):
        with patch.object(runtime.shutil, 'which', return_value=None), patch.object(Path, 'glob', return_value=[]):
            with self.assertRaisesRegex(ValueError, 'Node 22 is required'):
                runtime.environment({'runtime_requirements': ['node 22']})

    def test_malformed_requirement_is_not_ignored(self):
        with self.assertRaises(ValueError):
            runtime.environment({'runtime_requirements': ['node 22 and bun, each on its own line']})
