# Codex adapter acceptance evidence

## 2026-10-17 — native specialist implementation (0.29.0)

- Shared Python suite: 115 tests, 113 passed and two optional skips. Claude
  package assertions: 23 passed. Includes native TOML parsing for all eight
  profiles, ownership/idempotency, refusal to overwrite edited/user profiles,
  symlink protection, Git exclusion, exact native role lifecycle attribution,
  canonical tool callbacks and private command filtering.
- `python3 scripts/check_codex_host.py` ran against Codex CLI 0.145.0 in a
  disposable CODEX_HOME. Real marketplace registration and plugin installation
  succeeded; app-server skills/list discovered all eleven Abacus skills without
  discovery errors. Eight project profiles were written and parsed in tests.
- No model inference, live Studio credentials, client data, hook-trust changes,
  normal installation changes, pushes, PRs or deployments were performed.
- NOT yet verified: the host loading and executing a named profile in an actual
  model session; live trusted hook delivery; browser verification in Codex; the
  authenticated setup → edit → verify → Submit → Request publish journey.
  Generic workers stay unattributed. Never infer those acceptance results from
  the unit tests, profile files, or successful plugin discovery.
- Client test: update the released plugin, run approved Setup (or refresh the
  project's specialists), open a new chat in that workspace, request a structured
  feature using Spec Writer/Builder/Verifier, and open the optional local team
  dashboard with trusted hooks. Confirm real worker start/return, checks tied to
  the current code, Submit recovery point and publishing-review PR. Use a
  disposable sandbox app and stop before merge/deployment.

References: [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[Hooks](https://learn.chatgpt.com/docs/hooks). Custom agent files inherit host
permissions; behavioral role limits are not an independent tool sandbox.

## Historical preview evidence — 0.28.0

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
