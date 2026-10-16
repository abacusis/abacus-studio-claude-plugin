import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).parents[1]


class RoutingTests(unittest.TestCase):
    def test_hook_only_returns_constant_context_without_echoing_input(self):
        script = ROOT / 'scripts/route_development.py'
        first = subprocess.run([sys.executable, '-I', str(script)], input='untrusted arbitrary input', text=True, capture_output=True)
        second = subprocess.run([sys.executable, '-I', str(script)], input='{}', text=True, capture_output=True)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stderr, '')
        value = json.loads(first.stdout)
        self.assertEqual(set(value), {'hookSpecificOutput'})
        self.assertEqual(set(value['hookSpecificOutput']), {'hookEventName', 'additionalContext'})
        self.assertEqual(value['hookSpecificOutput']['hookEventName'], 'UserPromptSubmit')
        context = value['hookSpecificOutput']['additionalContext']
        self.assertIn('abacus-studio:engineering', context)
        self.assertIn('planning-only', context)
        self.assertIn('Do NOT activate Engineering for arithmetic', context)
        self.assertIn('Preserve planning-only boundaries and all approvals', context)
        self.assertIn('quick, deep, or automatic', context)
        self.assertIn('shortest adequate path', context)
        self.assertIn('No automatic', context)
        self.assertIn('never bypasses sensitive-work checks', context)
        self.assertNotIn('untrusted arbitrary input', first.stdout)

    def test_default_hook_is_bounded_and_fail_open(self):
        config = json.loads((ROOT / 'hooks/hooks.json').read_text())
        self.assertIn('UserPromptSubmit',config['hooks'])
        self.assertIn('SubagentStart',config['hooks'])
        self.assertIn('SubagentStop',config['hooks'])
        self.assertEqual(len(config['hooks']['UserPromptSubmit']), 1)
        hook = config['hooks']['UserPromptSubmit'][0]['hooks'][0]
        self.assertEqual(hook['type'], 'command')
        self.assertEqual(hook['timeout'], 5)
        self.assertTrue(hook['command'].endswith('|| exit 0'))
        self.assertIn('python3 -I', hook['command'])
        self.assertIn('|| python -I', hook['command'])
        for entries in config['hooks'].values():
            for entry in entries:
                for observer in entry['hooks']:
                    self.assertEqual(observer['timeout'],5)
                    self.assertTrue(observer['command'].endswith('|| exit 0'))
        # Default hooks/hooks.json discovery only: no duplicate registration.
        self.assertNotIn('hooks', json.loads((ROOT / '.claude-plugin/plugin.json').read_text()))

    @unittest.skipIf(os.name == 'nt', 'POSIX shell failure-path test; Windows validation separate')
    def test_missing_python_does_not_block_the_prompt(self):
        config = json.loads((ROOT / 'hooks/hooks.json').read_text())
        command = config['hooks']['UserPromptSubmit'][0]['hooks'][0]['command']
        with tempfile.TemporaryDirectory() as empty_path:
            result = subprocess.run(['/bin/sh', '-c', command], env={'PATH': empty_path, 'CLAUDE_PLUGIN_ROOT': str(ROOT)}, capture_output=True)
        self.assertEqual(result.returncode, 0)


if __name__ == '__main__': unittest.main()
