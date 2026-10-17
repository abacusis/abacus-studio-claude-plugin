---
name: abacus-request-publish
description: Send your sandbox changes for publishing review.
---

Resolve `<plugin-root>` from the absolute source path of this loaded skill: two directories above its directory. Substitute that real path in commands; it is not an environment variable. Skill references name packaged workflows, not a Claude Skill tool. Read references/codex/delegation.md before any specialist handoff; use approved project-scoped Abacus profiles when available.

Read and apply [Client communication](../../references/client-communication.md) completely.
Read [Request publish](../../references/changes/request-publish.md) completely and follow it.
Resolve scripts against `<plugin-root>/scripts/`.
Preview and review the PR; the user's request authorizes opening it. Do not ask
again about routine wording. Never merge or deploy. For “submit and publish,”
use `$abacus-submit` first under the same request. Request publish alone
does not authorize saving local edits.
