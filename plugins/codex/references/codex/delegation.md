# Codex delegation adapter

The eight role procedures in `roles/` reuse Abacus's specialist guidance. Approved
Setup installs project-local native profiles named `abacus-<role>` under
`.codex/agents/`. Use those exact names when listed in the current session; a new
session is required after setup/refresh. Do not request a namespaced Claude
agent or assume the plugin grants permission to spawn agents.

Where the current host permits delegation, use its documented native mechanism
with an available agent type. Give it the full relevant role instructions, the
authorized workspace, permitted actions, accepted criteria, source baseline,
existing edits to preserve, relevant curated knowledge and actual evidence.
Keep the client's configured model unless they request otherwise. Delegate only
independent reviews in parallel on stable code, with no concurrent Builder edits.
Wait for real results; do not call review agreement independent runtime proof.

Map the role's permitted operations to available host tools: Read/Grep/Glob mean
source inspection/search; Edit/Write mean authorized file editing; Bash means
approved command execution. A shell is not a workaround for a read-only role's
prohibited actions. Read-only reviewers cannot run tests, network requests or
target scripts. The Verifier may run approved checks but cannot fix application
code. UI review requires an actual image-capable tool; report unavailable otherwise.
Never alter host permissions, global config or agent profiles during development.
Profile installation/refresh belongs only to explicitly approved Setup through
`scripts/codex_agents.py`; it preserves conflicting and unrelated profiles.

Roles cannot delegate recursively. Report blocked instructions or unavailable
tools to the coordinator. Supply required instructions inline if the coordinator
has read them and the child cannot access the plugin directory. If delegation is
unavailable, denied or prohibited by current instructions, say so briefly and use
an honestly labeled main-conversation fallback where safe. Do not retry through
another tool to evade the restriction. A separate review explicitly required by
the user remains pending. Main-conversation work never masquerades as a subagent.

Codex hook agent_type may be a generic type rather than an Abacus role. Do not
infer role attribution from timing, a queued task, or a role mentioned in text.
The dashboard adapter recognizes exact native `abacus-<role>` profile names and
records their real start/return events. Generic child callbacks remain
unattributed; never fabricate a specialist map. Retain the client's model choice.
