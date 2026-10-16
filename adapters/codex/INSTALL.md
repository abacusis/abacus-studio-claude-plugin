# Abacus Studio for Codex — testing preview

This is the Codex package, not the repository's Claude package. Use the generated
`codex` branch explicitly; the default branch serves Claude. Do not copy files
into an existing Claude installation. This is a testing preview, not full parity
or an OpenAI public-directory listing.

## Install from GitHub

With a supported Codex CLI, run:

```sh
codex plugin marketplace add https://github.com/abacusis/abacus-studio-claude-plugin.git --ref codex
codex plugin add abacus-studio@abacus-studio-codex
```

These install the published Codex distribution, not the shared source checkout.
Then start a new Codex session and ask: “Set up my application with Abacus Studio.”

## Build a local test package (maintainers)

From a reviewed source checkout, build a new folder outside the repository:

```sh
python3 scripts/build_release.py --target codex --output /absolute/new/abacus-studio-codex
```

The output includes a Codex manifest, skills, shared helpers, specialist role
procedures, dashboard and a local marketplace. No setup or installation runs at
build time. Preserve the output folder while testing.

With a supported Codex CLI, add that generated marketplace, then install:

```sh
codex plugin marketplace add /absolute/new/abacus-studio-codex
codex plugin add abacus-studio@abacus-studio-codex
```

Review installation in the host. If your client does not support these commands,
use its plugin manager with the generated local marketplace. Start a new session
and check the installed skill's actual source path and manifest version. A source
checkout or an old cached plugin is not proof the new package is loaded.

Optional lifecycle hooks need separate host trust review. Never bypass hook trust
or change permissions merely to activate the dashboard. Without hooks, skills
remain usable; live observation and queued-action delivery are unavailable.
The first preview supports local Codex, not unattended cloud execution. Windows
hook execution requires a suitable python3 command; otherwise use skills without
hooks. No public directory submission or automatic updates are configured here.

## Use it

Ask naturally: “Set up my application with Abacus Studio.” Or select the packaged
`abacus-setup` skill. Studio opens browser approval; you choose the app, destination
and approve local installation/start commands. Do not paste credentials in chat.
You do not need a separate Studio MCP connector.

The helper authorization is shared with the Claude adapter on this computer.
Connecting renews it; Disconnect revokes it for both tools. Neither signs you out
of Codex itself or removes sandbox keys previously written into a local workspace.

- `abacus-connect`: sign in or renew Studio authorization.
- `abacus-disconnect`: revoke the shared helper connection, preserving files.
- `abacus-status`: only Studio connection, role and granted access.
- `abacus-setup`: clone the configured client repo and start a local preview.
- `abacus-engineering`: proportionate planning, building and verification.
- `abacus-design`: Studio-pinned project-local design guidance.
- `abacus-security`: focused source review, not a penetration test.
- `abacus-submit`: reviewed save/push to the client development branch.
- `abacus-request-publish`: request the review PR; no merge or deployment.

Project knowledge and sandbox database capabilities are used when relevant. Ask
for quick work, deeper review, a mockup only, or direct implementation normally.
Codex skills use the host's skill picker / `$skill-name` invocation, not Claude's
`/abacus-studio:` commands. Mutation approvals still apply.

Setup installs approved design skills into ignored `.agents/skills/`, not Claude's
folder. Existing skills are preserved; host-specific installation records prevent
one tool's copy from overwriting the other's. Preview metadata is stored under
`.studio/`; the helper can supervise startup when no host preview facility exists.

Specialist instructions use available authorized native delegation. They are not
installed custom-agent profiles or enforced tool allowlists. If delegation is
unavailable, Codex must disclose main-conversation work instead. The initial local
dashboard cannot attribute generic worker callbacks to Abacus roles; it omits
those workers rather than guessing. Hooks do not read private transcripts.

## Test before sharing

In a disposable app, ask for a quick text edit: expect no full team. Ask planning
only for a new screen: expect no edits and honest delegation capability. Ask for
a mockup only: expect labeled sample data and no backend writes. Ask for connection
status: expect no workspace scan or sign-in. With trusted hooks and approved local
tracking, open the dashboard and verify current main-session activity; don't infer
generic specialist visibility. Never use real customer records in these tests.

Production sign-in, real sandbox provisioning, migrations, submissions and publish
requests need separate authorized integration tests. Passing package tests does
not establish those live services work. To refresh the GitHub marketplace, run
`codex plugin marketplace upgrade abacus-studio-codex`, check the offered version
in your plugin manager and update/install it, then start a fresh session. For a
local build, create a fresh folder and re-add its marketplace. Do not assume an
already-running session picked up an update automatically.
