# Codex preview evidence — 0.28.0

2026-10-16, macOS. No client repository, live Studio app, credentials, migrations,
pushes, PRs or deployments were used. Existing normal tool installations were not
changed. Temporary CODEX_HOME held the test marketplace and plugin cache.

- Shared regression suite: 106 Python tests passed, including ten Codex adapter
  tests. Claude package suite: 21 passed. README and Claude manifest checks passed.
- Built a separate Codex ZIP with allowlisted files and verified checksums.
  Shared Python helpers and licenses remain byte-identical across packages.
- Native Codex CLI marketplace add and plugin add succeeded. An initial invalid
  authentication policy enum was rejected by the real host; corrected to ON_USE
  and successfully retested before claiming installation success.
- Codex app-server skills/list loaded all eleven installed skills with no discovery
errors, from the isolated cache's 0.28.0 source paths. No model inference or
  application development was run in this host discovery check.
- Unit tests exercise metadata filtering, isolated hook execution, interrupted
  versus successful states, unknown-event handling, separate skill receipts and
  preservation of the Claude package. These are not live trusted-hook evidence.

Still requires interactive acceptance: natural-language auto-routing, delegated
role behavior, hook trust and real lifecycle observation, browser/mockup behavior,
Studio authorization, real sandbox provisioning, Submit and Request publish.
Use disposable authorized apps and synthetic data. Do not turn these pending
checks into “all integrations verified” or a claim of full dashboard parity.

Generic Codex workers are not attributed to specialist roles. No runtime-enforced
role tool allowlists, model-independent workflow enforcement, unattended execution,
automatic cloud recovery or universal-directory publication is implemented.

The standalone skill-creator validator could not run because its Python runtime
lacked PyYAML; no dependency was installed. Native Codex skill discovery parsed
the installed skills successfully, but that is not a behavioral evaluation.

Packaging follows official documentation:
[Codex plugin packaging](https://developers.openai.com/plugins/build/plugins),
[Claude migration](https://developers.openai.com/plugins/guides/submit-claude-plugin),
[Hooks and trust](https://learn.chatgpt.com/docs/hooks).
