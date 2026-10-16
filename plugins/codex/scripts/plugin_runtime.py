"""Package-selected host paths; no user config, credentials or global mutation."""
from pathlib import Path


def is_codex():
    return (Path(__file__).resolve().parents[1] / '.codex-plugin/plugin.json').is_file()


def skills_directory():
    return '.agents' if is_codex() else '.claude'


def launch_path(root):
    return Path(root) / ('.studio/codex-preview.json' if is_codex() else '.claude/launch.json')


def skill_state(root, name):
    base = Path(root) / '.studio/skills'
    return base / 'codex' / (name + '.json') if is_codex() else base / (name + '.json')
