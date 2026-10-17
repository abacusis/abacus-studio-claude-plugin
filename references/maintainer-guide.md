# Plugin maintainer guide

Client introduction: [README](../README.md). Release checklist:
[RELEASE](../RELEASE.md). Access boundaries: [SECURITY](../SECURITY.md).

Review and update the public README in every change set. Highlight real client
value without inventing features, and keep latest version, availability and the
specialist team current. Repository AGENTS.md defines the standing rule; the
README CI workflow checks changed-file coverage, and release packaging validates
version and specialist introductions. Run `python3 scripts/check_readme.py`
before handoff. These checks do not replace editorial review.

## Tool adapter maintenance (not client setup)

Client guides live at adapters/claude/INSTALL.md and adapters/codex/INSTALL.md.
Root INSTALL.md is a short tool chooser. Both generated packages put their own
guide at INSTALL.md in the package root; do not hand-edit generated copies.
Keep them focused on installation, connection, setup, saving and publishing review.
Do not put package building, developer acceptance tests or publisher checklists
in those guides. The Claude adapter overview links to its adjacent client guide.

Shared sources stay in skills/, agents/, references/ and scripts/. Claude's
adapter renders them with scripts/build_claude.py; the root Claude marketplace
selects plugins/claude. Codex uses scripts/build_codex.py and plugins/codex.
Run `python3 scripts/generate_packages.py`, then `--check`; never hand-edit the
generated distributions. Standalone ZIP catalogs select their own package root.

For a local Codex test package, choose a new folder outside the checkout:

```sh
python3 scripts/build_release.py --target codex --output /absolute/new/abacus-studio-codex
codex plugin marketplace add /absolute/new/abacus-studio-codex
codex plugin add abacus-studio@abacus-studio-codex
```

Use an isolated profile for maintainer tests. Preserve the output folder and
verify the installed skill source path and manifest, not just a source checkout.
See adapters/codex/TESTING.md for executed evidence and pending acceptance.
Exercise quick edits, planning-only and mockup-only requests, connection status,
and optional dashboard tracking in disposable authorized projects with synthetic
data. Live authorization, provisioning, migrations, submissions and publishing
requests require separate in-scope integration tests. Unit tests do not establish
those live services work.

Codex specialist roles are procedures, not registered Claude agent profiles or
enforced tool allowlists. Generic worker callbacks cannot be mapped to roles.
Hook trust is separate; do not bypass it. Without trusted hooks, live observation
and queued-action delivery are unavailable. Windows needs a suitable python3;
do not claim unattended/cloud operation or dashboard parity. Detailed boundaries
remain in adapters/codex/delegation.md and the generated TESTING.md.

For older Codex sources pinned to the removed codex branch, re-register the
marketplace once: `codex plugin marketplace remove abacus-studio-codex`, then
the current GitHub marketplace-add and plugin-add commands from the client guide.
This changes plugin registration, not application files. Do not remove a working
default-branch installation simply because GitHub renamed its repository.
For old ZIP copies, disable the duplicate before enabling a marketplace copy;
never delete application workspaces as part of plugin replacement.

Publisher checks and version/tag procedures stay in RELEASE.md. Keep credentials,
environment files, caches and client application code out of every distribution.

## Capability references

- [Coordinator workflow — Steps 1 through 9](engineering/orchestration.md): local main-session
  coordination, role selection, evidence, bounded correction, and readiness.
  Spec Writer, Builder, Verifier, Code Reviewer, Security Reviewer, UI Reviewer,
  UX Reviewer and Readiness Reviewer are bundled; quality-check hooks, dashboard,
  and progress upload are not implemented yet. The agent inherits the session model.
  See [manual acceptance checks](engineering/orchestration-testing.md).

- [Client communication](client-communication.md): every bundled skill loads the
  plain-language standard. This is model guidance, not a global output filter.
- [Application code map](engineering/code-map.md): optional pinned Graphify runtime,
  local source-only snapshots, freshness checks, bounded queries, and fallback.
- [Application knowledge](app-knowledge.md): explicit sharing, lifecycle-aware
  search/get, current approved guidance versus proposed or superseded context.
- [Specification-driven planning](engineering/specification.md): larger features
  use specifications, implementation tasks, and acceptance evidence.
- [Focused security review](security/review.md): source review, not a complete
  audit harness, live penetration test, or Studio Health reporting integration.
- [Local browser verification](engineering/browser-verification.md): reuse host
  browser tools or an approved managed Python Playwright/Chromium installation.
  Screenshots stay local and require actual image inspection; no browser profile
  reuse, automatic login, trace upload, or unapproved form submission.

## Studio deployment dependencies

Version 0.17.1 adds a local routing-only UserPromptSubmit hook in hooks/hooks.json.
It emits constant context without reading the prompt, credentials, source, or
transcripts; no network, writes, uploads, or background service. Python 3 is tried
as python3 then python; failure returns to normal processing. It does not grant
permissions or block a prompt. Hosts can disable hooks, and model selection is
still probabilistic. No backend migration or setup reinstall is required, but
the updated plugin must be loaded in a fresh/reloaded session. Test ordinary
prompts and actual Skill/agent activity, not just explicit slash commands.

For code mapping, apply migration `20261015020000_workspace_code_map.sql`, deploy
`admin-projects`, `mcp`, and `local-git`, then release the settings frontend.
The per-application option defaults to disabled. Approved Setup must disclose
installation; do not silently enable it for existing clients.

Knowledge requires the matching backend and
`20261015010000_app_knowledge_library.sql`. Existing records are not automatically
shared. See the knowledge reference for visibility and approval rules.
The communication update needs no backend deployment.
Version 0.18.0's Builder and browser helpers also need no backend change. The helper
uses existing local-workspace authorization, with separate install/capture actions.
Windows/Linux end-to-end browser validation remains outstanding; browser runtime
installation never installs OS packages or assumes unsupported platforms work.

## Operational notes

Connect and Setup share helper authorization in OS credential storage. No separate
Claude connector sign-in or `/mcp` is required. Legacy connectors and older per-app
consents remain independent. Status checks connection, roles, and granted access
only; it must not scan workspaces or initiate sign-in.

GitHub credentials are repository-scoped, not branch-scoped. Review repository
rules and deployment hooks rather than assuming all pushes are isolated.
Submission preserves fetch-first, reviewed conflicts, configured checks, and push
approval. Secret detection is best effort. Submodule and Git LFS setup are not
supported. No automatic conflict winner, force push, merge, or deployment occurs.

Sandbox environment files are Git-ignored but readable by local users and coding
tools. Management tokens remain in Studio. Removing stored sandbox secrets does
not revoke provisioned copies; rotate them at the provider. Required Next.js
public variable aliases never contain privileged server secrets.

Missing prerequisites require installation approval; there is no plaintext token
fallback. Windows/Linux end-to-end validation remains required before broad
rollout. Cross-platform code alone does not establish platform verification.

## Validation

```sh
node --test tests/package.test.mjs
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p '*test*.py'
claude plugin validate .
```

See RELEASE.md for allowlisted packaging and publication. Preserve upstream
notices. The current Abacus LICENSE is explicitly a draft, not adopted terms;
do not describe it as an effective commercial license.
