# Local team dashboard in Codex

Read [Shared dashboard contract](local-dashboard-shared.md) before enabling.
Its privacy, opt-in tracking, loopback capability, Git read-only and separate
action approval requirements remain unchanged. Use actual absolute plugin paths.

This package includes optional Codex lifecycle hooks. Installation does not trust
them: the client must review/approve them in the supported host. Never change
trust settings or bypass hook trust automatically. Without trusted hooks, the
dashboard can show local Git status but cannot observe agent/session activity or
deliver queued actions. Say so; do not claim a live team or invent a session key.
Automatic Engineering skill discovery still works without hooks.

The adapter handles SessionStart, UserPromptSubmit, SubagentStart/SubagentStop,
PreToolUse/PostToolUse, Interrupt, Stop and SessionEnd. It records only bounded
metadata, never prompts, transcripts, commands, patches, reasoning or tool output.
Codex shell tool events show a generic command action; their text is discarded.
apply_patch events show an edit action but do not infer files or per-file counts
from patch content. Only recognizable Abacus agent types can be role-attributed.
Codex generic workers may therefore be absent from the team map. Coordinator
reports remain labeled as reports, not independently observed child execution.

Use the actual hook-provided session key for reports. Never manufacture lifecycle
callbacks from the conversation, read transcript files, or relabel generic worker
events to make the display look complete. Unsupported tool callbacks are omitted.
Returning an agent does not prove its checks passed. Stop means turn finished,
not publication. Interrupted/stale sessions do not promise continuing work.

Submit/Request publish buttons queue intents only. Return to Codex and send
Continue; a trusted UserPromptSubmit hook delivers them. Follow the existing
workflows, checks and confirmations. With hooks unavailable, ask Codex directly.
The server does not send prompts or start another Codex process. No live source
diffs, transcript mirroring, cloud execution or automatic publication is added.
