import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_release
import build_codex
import codex_hook
import install_skills
import plugin_runtime
import local_dashboard
import test_install_skills as skill_fixtures


class CodexPackageTests(unittest.TestCase):
    def test_package_has_codex_skills_roles_and_no_claude_entrypoints(self):
        with tempfile.TemporaryDirectory() as temp:
            result = build_release.build(ROOT, Path(temp) / 'codex', 'codex')
            with zipfile.ZipFile(result['zip']) as archive:
                names = set(archive.namelist())
                self.assertFalse(any(n.startswith(('.claude-plugin/', 'agents/')) for n in names))
                manifest = json.loads(archive.read('.codex-plugin/plugin.json'))
                self.assertEqual(manifest['skills'], './skills/')
                self.assertEqual(manifest['hooks'], './hooks/hooks.json')
                self.assertEqual(manifest['version'], json.loads((ROOT / '.claude-plugin/plugin.json').read_text())['version'])
                for skill in build_codex.SKILLS:
                    content = archive.read(f'skills/abacus-{skill}/SKILL.md').decode()
                    self.assertNotIn('${CLAUDE_PLUGIN_ROOT}', content)
                    self.assertNotIn('/abacus-studio:', content)
                    self.assertNotIn('$ARGUMENTS', content)
                for role in build_codex.ROLES:
                    self.assertIn(f'roles/{role}.md', names)
                for path in ('scripts/studio_git.py', 'scripts/plugin_runtime.py', 'scripts/codex_hook.py',
                             'scripts/browser_verification.py', 'scripts/install_skills.py', 'LICENSE', 'THIRD_PARTY_NOTICES.md'):
                    self.assertEqual(archive.read(path), (ROOT / path).read_bytes())
                self.assertIn('skills/abacus-setup/agents/openai.yaml', names)
                for skill in build_codex.SKILLS:
                    metadata = archive.read(f'skills/abacus-{skill}/agents/openai.yaml').decode()
                    self.assertIn(f'display_name: "{skill.replace("-", " ").title()}"', metadata)
                    self.assertNotIn('display_name: "Abacus', metadata)
                    self.assertIn(f'Use $abacus-{skill}', metadata)
                    self.assertEqual('allow_implicit_invocation: false' in metadata,
                                     'disable-model-invocation: true' in (ROOT / f'skills/{skill}/SKILL.md').read_text())
                catalog = json.loads(archive.read('.agents/plugins/marketplace.json'))
                self.assertEqual(catalog['plugins'][0]['source']['path'], './')
                self.assertEqual(catalog['plugins'][0]['policy']['authentication'], 'ON_USE')
                self.assertIsNone(archive.testzip())
            with self.assertRaises(ValueError):
                build_release.build(ROOT, Path(temp) / 'codex', 'codex')

    def test_claude_default_stays_claude(self):
        with tempfile.TemporaryDirectory() as temp:
            result = build_release.build(ROOT, Path(temp) / 'claude')
            with zipfile.ZipFile(result['zip']) as archive:
                self.assertEqual(archive.read('skills/engineering/SKILL.md'), (ROOT / 'skills/engineering/SKILL.md').read_bytes())
                self.assertEqual(archive.read('hooks/hooks.json'), (ROOT / 'hooks/hooks.json').read_bytes())
                self.assertNotIn('.codex-plugin/plugin.json', archive.namelist())

    def test_host_paths_selected_by_installed_package_not_user_environment(self):
        self.assertFalse(plugin_runtime.is_codex())
        with patch.object(plugin_runtime, 'is_codex', return_value=True):
            self.assertEqual(plugin_runtime.skills_directory(), '.agents')
            self.assertEqual(plugin_runtime.launch_path('/example'), Path('/example/.studio/codex-preview.json'))
            self.assertEqual(plugin_runtime.skill_state('/example', 'impeccable'), Path('/example/.studio/skills/codex/impeccable.json'))
        with tempfile.TemporaryDirectory() as temp:
            result = build_release.build(ROOT, Path(temp) / 'codex', 'codex')
            check = subprocess.run([sys.executable, '-c',
                'import plugin_runtime; assert plugin_runtime.is_codex(); assert plugin_runtime.skills_directory()==".agents"'],
                cwd=Path(result['folder']) / 'scripts', capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stderr)

    def test_codex_install_preserves_claude_copy_and_uses_separate_receipt(self):
        fixture = skill_fixtures.SkillTests()
        fixture.setUp()
        try:
            config, data = fixture.config()
            install_skills.install(fixture.root, config, lambda _: data)
            with patch.object(plugin_runtime, 'is_codex', return_value=True):
                installed = install_skills.install(fixture.root, config, lambda _: data)
                self.assertEqual(installed[0]['state'], 'installed')
                self.assertTrue((fixture.root / '.agents/skills/design/SKILL.md').is_file())
                self.assertTrue((fixture.root / '.studio/skills/codex/design.json').is_file())
            self.assertTrue((fixture.root / '.claude/skills/design/SKILL.md').is_file())
        finally:
            fixture.doCleanups()

    def test_codex_preview_writes_private_metadata_not_claude_launch_file(self):
        import preview_workspace
        with tempfile.TemporaryDirectory() as temp, patch.object(plugin_runtime, 'is_codex', return_value=True):
            root = Path(temp)
            (root / '.studio').mkdir()
            with patch.object(preview_workspace, 'environment', return_value=dict(__import__('os').environ)):
                _, entry = preview_workspace.refresh_launch(root, {'commands': {'start': 'npm run dev -- --port 3002'}})
            self.assertEqual(entry['port'], 3002)
            self.assertTrue((root / '.studio/codex-preview.json').is_file())
            self.assertFalse((root / '.claude').exists())


class CodexHookTests(unittest.TestCase):
    def test_observation_is_opt_in_and_generic_workers_do_not_become_specialists(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            base = {'cwd': str(root), 'session_id': 'codex-test', 'hook_event_name': 'UserPromptSubmit', 'prompt': 'PRIVATE'}
            codex_hook.handle(base)
            self.assertFalse((root / '.studio').exists())
            (root / '.git/info/exclude').write_text('/.studio/\n')
            local_dashboard.enable(root, approved=True)
            result = codex_hook.handle(base)
            self.assertIn('Dashboard session key', result['hookSpecificOutput']['additionalContext'])
            codex_hook.handle(base | {'hook_event_name': 'SubagentStart', 'agent_type': 'default', 'agent_id': 'child'})
            codex_hook.handle(base | {'hook_event_name': 'PostToolUse', 'tool_name': 'apply_patch', 'tool_input': {'patch': 'PRIVATE'}})
            state = local_dashboard.snapshot(root)
            self.assertNotIn('PRIVATE', json.dumps(state))
            self.assertFalse(any(a['invoked'] for a in state['agents']))
            self.assertTrue(any(e['summary'] == 'Edited a file' for e in state['events']))
            codex_hook.handle(base | {'hook_event_name': 'Interrupt'})
            self.assertEqual(local_dashboard.snapshot(root)['session']['state'], 'attention')

    def test_private_inputs_never_forwarded_and_unknown_events_omitted(self):
        raw = {'cwd': '/example', 'session_id': 's', 'hook_event_name': 'PostToolUse',
               'tool_name': 'apply_patch', 'tool_input': {'patch': 'PRIVATE'},
               'prompt': 'PRIVATE', 'transcript_path': '/private/transcript', 'tool_response': 'PRIVATE'}
        clean = codex_hook.adapt(raw)
        self.assertEqual(clean['tool_name'], 'Edit')
        self.assertEqual(clean['tool_input'], {})
        self.assertNotIn('PRIVATE', json.dumps(clean))
        self.assertNotIn('transcript', json.dumps(clean))
        self.assertIsNone(codex_hook.adapt(raw | {'tool_name': 'unknown'}))
        self.assertIsNone(codex_hook.adapt(raw | {'hook_event_name': 'Unknown'}))

    def test_routing_works_without_dashboard_but_never_executes_work(self):
        received = []
        def disabled(value):
            received.append(value)
            raise ValueError('not enabled')
        result = codex_hook.handle({'hook_event_name': 'UserPromptSubmit', 'prompt': 'PRIVATE'}, disabled)
        self.assertIn('abacus-engineering', result['hookSpecificOutput']['additionalContext'])
        self.assertNotIn('PRIVATE', json.dumps(received))
        self.assertNotIn('prompt', received[0])

    def test_interrupt_is_not_success_and_generic_agent_is_not_relabelled(self):
        event = {'cwd': '/example', 'session_id': 's', 'hook_event_name': 'Interrupt'}
        self.assertEqual(codex_hook.adapt(event)['hook_event_name'], 'StopFailure')
        event.update(hook_event_name='SubagentStart', agent_type='default', agent_id='child')
        self.assertEqual(codex_hook.adapt(event)['agent_type'], 'default')

    def test_isolated_hook_invocation(self):
        result = subprocess.run([sys.executable, '-I', str(ROOT / 'scripts/codex_hook.py')],
                                input=json.dumps({'hook_event_name': 'UserPromptSubmit'}),
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('abacus-engineering', json.loads(result.stdout)['hookSpecificOutput']['additionalContext'])
