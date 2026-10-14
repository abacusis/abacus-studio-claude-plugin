# Abacus Studio — Claude Code plugin 0.14.0

Substantial features now use specification-driven planning inside Engineering:
agree on business requirements, plan implementation, create traceable tasks, and
verify the result against acceptance criteria. Small edits stay lightweight.
No new commands or Spec Kit installation are required. Specs use the project's
existing documentation convention (or an approved location); they are ordinary
reviewed source-repository documents, not automatically uploaded to Studio.
See [planning workflow](references/engineering/specification.md) and
[Spec Kit attribution](references/engineering/spec-kit-upstream.md).

## Abacus Security

Focused source-based security reviews are automatically discoverable or available
through `/abacus-studio:security`. Engineering routes security-sensitive changes
to this guidance. Reviews report evidence and unresolved validation separately;
they do not modify source, run target code, probe live systems, or guarantee safety.
This is a curated Cloudflare-informed adaptation, not the complete upstream audit
harness. Full audit execution, validated JSON reports, and Studio Health uploads
are not included. See [provenance and license](references/security/upstream.md).

## Abacus Engineering

Bundled engineering guidance is available automatically for relevant development
work, or through `/abacus-studio:engineering`. It covers requirements and project
language, behavior-first testing, evidence-led debugging, maintainable architecture,
and requirements/engineering review. No separate upstream plugin installation is
needed. Design stays with Impeccable; saving and publishing stay with Studio.

This package does not automatically commit, push, migrate, or deploy. It does not
add credentials, hooks, a background service, or Studio dashboard reporting.
See [provenance and MIT notice](references/engineering/upstream.md).

Next.js apps receive public Supabase variable aliases requested by Studio's
Required environment variable names, including NEXT_PUBLIC_SUPABASE_URL and
NEXT_PUBLIC_SUPABASE_ANON_KEY. Privileged server secrets are never public aliases.

Connect opens one Studio browser approval for app access and local development.
Setup reuses it. No Claude connector sign-in or `/mcp` is required; the helper
calls Studio's MCP service privately using OS-stored tokens.

## Commands

Choose an action directly from the Abacus Studio plugin menu:

| Command | Purpose |
| --- | --- |
| `/abacus-studio:connect` | Sign in or renew authorization. |
| `/abacus-studio:disconnect` | Disconnect Studio and selected local authorization. |
| `/abacus-studio:status` | Show connection, role, and granted access only. |
| `/abacus-studio:setup` | Choose an app, clone its code, and open a local preview. |
| `/abacus-studio:design` | Improve the interface. Describe your goal in plain language. |
| `/abacus-studio:engineering` | Plan, build, debug, test, or review a change. Claude can also select it automatically. |
| `/abacus-studio:security` | Review source for security boundary failures without changing or executing the application. |
| `/abacus-studio:submit` | Review and save changes to the sandbox repository. |
| `/abacus-studio:request-publish` | Request a publishing review PR. |

Setup works directly; Connect does not have to be run first. Setup and Connect
accept an optional app name. Design accepts a plain-language goal or an optional
action such as `audit`. No required subcommands remain.

The workspace and changes group commands have been removed. Migrations are an
internal skill Claude can select when needed, using Studio's reviewed sandbox
workflow. Clients do not need to remember a migration command. Migration SQL
still requires explicit review and approval.

## Install and use

See [installation instructions](INSTALL.md) for ZIP upload and marketplace setup.
Replace the installed plugin and start a new session to refresh the menu.
The distribution repository is `abacusis/abacus-studio-claude-plugin`.

Install from a local Claude Code session:

```text
/plugin marketplace add abacusis/abacus-studio-claude-plugin
/plugin install abacus-studio@abacus-studio-marketplace
```

Claude Code 2.1.275 or later also supports the combined install:
`/plugin install abacus-studio --marketplace abacusis/abacus-studio-claude-plugin`.

1. Run Setup, select an app, and approve the local folder and setup commands.
2. Complete the browser approval opened by Connect or Setup once.
3. Preview and build with Claude. Use Design for interface improvements.
4. Submit fetches first, reviews all outgoing changes, resolves conflicts with
   approval, runs configured checks, and confirms a normal push to sandbox.
5. Request publish opens a review PR. It does not merge or deploy.

Status checks only Studio authentication, current roles, and granted permissions.
It never searches folders, fetches Git, or starts sign-in. Connect resets the
shared helper authorization before listing apps. Disconnect revokes that shared
authorization. Older connector and legacy per-app consents remain separate.

## Setup and access

Studio supplies the separate private client repository, sandbox branch, commands,
Node requirements, enabled skill packages, and optional sandbox credentials.
Setup checks Git, Python, and secure OS credential storage, selecting the private
`~/.abacus-studio/venv` automatically when default Python lacks keyring.
Missing prerequisites require installation approval. There is no plaintext token
fallback. Windows/Linux end-to-end testing remains required before broad rollout.

Setup refreshes Studio settings before starting the preview and verifies HTTP,
process survival, and browser rendering. Existing snapshots and local files are
preserved. Project skill packages are pinned and installed into ignored local
folders without running upstream installers or enabling hooks.

Studio checks membership and repository authorization for credential requests.
GitHub credentials are repository scoped, not branch scoped; use GitHub rulesets
for branch enforcement. Source changes go through Git, while Studio stores activity
metadata. Review deployment hooks before treating repository pushes as isolated.

Optional sandbox credentials are provisioned into a Git-ignored `.env`; local
users and coding tools can read them. Management tokens remain in Studio.
Never configure production credentials. Removing stored secrets does not revoke
local copies; rotate them in Supabase when access ends.

Secret detection is best effort. Known local/generated/secret paths and workflow
changes are blocked from submission. No force push, background autosync,
automatic conflict winner, merge, or production deployment is performed.
Submodules and Git LFS setup are not supported. Preserve failed operation state
and ask the administrator to inspect uncertain migration outcomes.

## Validation

`node --test tests/package.test.mjs`

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p '*test*.py'`

`claude plugin validate .claude-plugin/plugin.json`

Publisher: see [release preparation](RELEASE.md) and [security boundaries](SECURITY.md).
