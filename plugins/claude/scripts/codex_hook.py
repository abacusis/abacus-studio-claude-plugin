"""Codex event adapter: bounded metadata only; never inspect transcripts or inputs."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from local_dashboard import observe
from codex_agents import ROLES

ROUTING = (
    'Abacus Studio for Codex: for application planning, changes, debugging, tests '
    'or review, read the packaged abacus-engineering skill first. Honor quick/deep '
    'intent; small low-risk edits stay focused with no automatic team. Use optional '
    'mockup-first guidance only when relevant; mockup-only grants no backend work. '
    'Use native delegation only when available and authorized, with the packaged '
    'role instructions; never invent installed Claude agents. Status is connection '
    'and role only. Preserve approvals for setup, data writes, submission and '
    'publishing. Keep client replies brief. No permissions are granted by this hook.'
)


def adapt(payload):
    if not isinstance(payload, dict):
        return None
    kind = payload.get('hook_event_name')
    supported = {'SessionStart', 'UserPromptSubmit', 'SubagentStart', 'SubagentStop',
                 'PreToolUse', 'PostToolUse', 'Interrupt', 'Stop', 'SessionEnd'}
    if kind not in supported:
        return None
    clean = {k: payload[k] for k in ('cwd', 'session_id', 'agent_id', 'agent_type') if k in payload}
    clean['hook_event_name'] = 'StopFailure' if kind == 'Interrupt' else kind
    # Native project profiles have an exact, generated name. Never guess a role
    # from worker text, task names, timing, prompts or transcript content.
    profile = payload.get('agent_type', '')
    if profile in {'abacus-' + role for role in ROLES}:
        clean['agent_type'] = 'abacus-studio:' + profile.removeprefix('abacus-')
    if kind in ('PreToolUse', 'PostToolUse'):
        names = {'exec_command': 'Bash', 'shell_command': 'Bash', 'shell': 'Bash', 'Bash': 'Bash',
                 'apply_patch': 'Edit', 'Edit': 'Edit', 'Write': 'Write',
                 'Read': 'Read', 'Grep': 'Grep', 'Glob': 'Glob',
                 'Agent': 'Agent', 'spawn_agent': 'Agent'}
        tool = names.get(payload.get('tool_name'))
        if not tool:
            return None
        clean['tool_name'] = tool
        clean['tool_input'] = {}
    return clean


def handle(payload, observer=observe):
    clean = adapt(payload)
    if clean is None:
        return None
    context = ''
    try:
        result = observer(clean)
        if result:
            context = result.get('hookSpecificOutput', {}).get('additionalContext', '')
    except Exception:
        pass
    if payload.get('hook_event_name') == 'UserPromptSubmit':
        context = ROUTING + (' ' + context if context else '')
    if context:
        return {'hookSpecificOutput': {'hookEventName': payload['hook_event_name'],
                                       'additionalContext': context}}
    return None


if __name__ == '__main__':
    try:
        raw = sys.stdin.buffer.read(1048577)
        if len(raw) <= 1048576:
            result = handle(json.loads(raw))
            if result:
                print(json.dumps(result))
    except Exception:
        pass
