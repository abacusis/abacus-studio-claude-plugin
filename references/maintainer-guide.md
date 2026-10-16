# Plugin maintainer guide

Client introduction: [README](../README.md). Release checklist:
[RELEASE](../RELEASE.md). Access boundaries: [SECURITY](../SECURITY.md).

## Capability references

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

## Studio deployment dependencies

For code mapping, apply migration `20261015020000_workspace_code_map.sql`, deploy
`admin-projects`, `mcp`, and `local-git`, then release the settings frontend.
The per-application option defaults to disabled. Approved Setup must disclose
installation; do not silently enable it for existing clients.

Knowledge requires the matching backend and
`20261015010000_app_knowledge_library.sql`. Existing records are not automatically
shared. See the knowledge reference for visibility and approval rules.
The communication update needs no backend deployment.

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
