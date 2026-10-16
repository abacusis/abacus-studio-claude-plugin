# Local team dashboard

Use when the client asks to see the team, activity, checks, local changes or open
the dashboard. No new slash command. It is optional; connection Status must remain
limited to Studio connection/role, never launch this or scan workspaces implicitly.

## Open within informed local approval

Work only in the selected authorized Git root. Explain that enabling the dashboard
records local activity metadata and starts a loopback server; approved screenshot
and AI image-read rules still apply. Existing setup approval can include this;
otherwise obtain approval before enabling. No global installer or new dependency.
Use the same approved helper Python as Setup, not a guessed missing environment.

`python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/local_dashboard.py" start --workspace "<authorized Git root>" --approved`

The root's `.studio/` must already be Git-ignored. If not, explain the needed local
exclusion and get approval to add `.studio/` to that repository's local Git exclude
file through normal file tools. Do not silently change source or commit ignore rules.
The helper returns the local capability URL and identified server PID. Open that
URL in the available browser, never a remembered port. Keep the URL local; it gives
read access to this workspace's dashboard and can queue allowed workflow requests.
Never reuse a server from another project or stop unrelated listeners.

## What is observed

Only an enabled root records lifecycle and bounded tool metadata from the bundled
Claude hooks. The Orchestrator stays visible; specialists appear when invoked or
given a reported task and remain muted after finishing. Unused roles stay hidden.
"Finished task" means returned, not passed. PreToolUse supplies current actions.

The coordination map connects only observed invocations to the session
Orchestrator. Queued reports alone do not establish a handoff. New start/return
callbacks can produce a single directional signal; initial history and unchanged
polls do not replay it. Reduced motion, offline, stale events and ended sessions
do not animate. Lines represent session coordination, not access to private agent
messages or proof that every invocation was spawned directly by the main thread.

Read/Edit/Write can supply filtered file paths. No command text or search pattern
is exposed. The activity list omits generic lifecycle-only noise. Start
and return events reflect actual callbacks, not model assurances. Multiple active
instances have a count. An agent returning does not imply success. After five
minutes without an agent signal it is labeled No recent signal; this may mean a
long-running command, not a proven disconnect. SessionEnd interrupts remaining
working states. The server can stay open without keeping Claude agents running.

No prompts, transcripts, raw tool inputs/results, command text, private reasoning,
credentials or file contents are stored. Filtered source paths may be recorded
for Read/Edit/Write. Only successful Edit/Write events count as attributed changes,
never reads or pre-action attempts. Missing IDs mean no per-agent attribution;
do not fabricate it. Hooks outside the enabled root or unsupported/disabled hooks
cannot supply activity. No events means no session yet, not a healthy live connection.
History is bounded to 2,000 events; it is not durable job recovery or a full audit log.

## Coordinator reports

The SessionStart/UserPromptSubmit context provides a dashboard session key. Use it
for the CURRENT session, not a guessed/latest key from another conversation. The
main coordinator MUST report a short task before each authorized delegation
with `status: "queued"` and no checks/findings. The next observed start consumes
that assignment, so the task remains current without refreshing old evidence.
and update its result after receiving the specialist's response, when the dashboard
is enabled and the host permits helper execution. Also update the Orchestrator's
summary at meaningful stage transitions. Describe the goal in plain language,
not tool names. Do not emit a helper call for every file read or test line.
Reporting failure must not block development or change permissions; disclose
missing details instead of inventing a task. Checks/findings must reflect actual
evidence. Omit secrets and customer data.
Reports are explicitly coordinator-reported, not independently executed checks.
Use `report` with reviewed JSON on stdin, no interpolation of client text:

`python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/local_dashboard.py" report --workspace "<root>" --session "<hook-provided key>"`

Example: `{"role":"verifier","summary":"Checking form recovery","checks":[{"title":"Failed save keeps input","result":"failed"},{"title":"Keyboard flow","result":"not_verified"}]}`

Before delegation: `{"role":"builder","summary":"Add required-name validation","status":"queued"}`.

Roles use bundled agent names or `orchestrator`. Results: passed, failed,
not_verified, blocked, note. A report cannot invent working/returned lifecycle
states. If no hook key or observer is available, disclose the gap and use chat.
Never add Bash/Write permissions to read-only reviewers for reporting: the main
coordinator calls the helper. Preserve affected-source freshness; after relevant
edits refresh checks and reports, and flag stale evidence. An agent restart makes
older reports stale automatically; other code edits still require coordinator care.

## Git and actions

Local changes are read-only Git status, excluding hidden/credential/generated paths.
Unpushed commits are a cached upstream comparison, not a current GitHub check.
No upstream or Git failure means unknown—not zero. No fetch, source diffs, commit
messages, credentials, push or publication lookup runs to populate the dashboard.
A clean tree does not mean pushed; neither state implies production publication.

Submit changes and Request publish queue only those two allowlisted intents in
local metadata. They do NOT run Git/SQL/commands or send a message to Claude.
The client returns to Claude and sends Continue; the next UserPromptSubmit hook
delivers the request once. Follow the existing Submit/Request publish workflow,
with its required checks and separate approvals. The click is not commit/push or
publishing approval. Delivered is not executed/succeeded. If hooks are unavailable,
ask Claude directly with the existing command; do not launch a new headless session
or bypass approvals. Pause, live question answering, cloud backup/release status
and code diffs are not included in this version.

## Close or disable

With authorization stop ONLY the identified dashboard server via its local
capability endpoint:
`python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/local_dashboard.py" stop --workspace "<root>" --approved`

Disable future recording separately with `disable --workspace "<root>" --approved`.
This preserves existing local history and files. No automatic deletion, process
killing, Git mutation, cloud upload or execution recovery. A local observer is not
a sandbox: existing host permissions and data-handling rules remain in force.
