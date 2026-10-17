---
name: abacus-submit
description: Review your changes and save them to the sandbox repository.
---

Resolve `<plugin-root>` from the absolute source path of this loaded skill: two directories above its directory. Substitute that real path in commands; it is not an environment variable. Skill references name packaged workflows, not a Claude Skill tool. Read references/codex/delegation.md before any specialist handoff; use approved project-scoped Abacus profiles when available.

Read and apply [Client communication](../../references/client-communication.md) completely.
Read [Submit](../../references/changes/submit.md) completely and follow it.
Resolve scripts against `<plugin-root>/scripts/`.
Preserve fetch-first, diff review, conflict resolution and checks. The user's
Submit request authorizes normal commit/check/push steps; do not re-ask approval.
For “submit and publish,” continue to `$abacus-request-publish` under the
same request. Submit alone does not authorize opening a review PR.
