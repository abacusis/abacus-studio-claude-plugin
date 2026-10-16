# Claude adapter

Shared Claude-compatible instructions remain in the source skills/, agents/ and
references/ folders. scripts/build_claude.py packages them without changing agent
tool scopes, workflow permissions or hook behavior. The root .claude-plugin
marketplace selects plugins/claude; the standalone ZIP selects its own root.

Run `python3 scripts/generate_packages.py` from the source checkout to regenerate
both tool packages, then run it with `--check`. Never hand-edit plugins/claude.
Codex follows the same adapters/<tool>, build_<tool>.py, plugins/<tool> convention.
See the root INSTALL.md for client installation; no new Claude commands are needed.
