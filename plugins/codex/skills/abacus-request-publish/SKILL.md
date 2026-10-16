---
name: abacus-request-publish
description: Send your sandbox changes for publishing review.
---

Resolve `<plugin-root>` from the absolute source path of this loaded skill: two directories above its directory. Substitute that real path in commands; it is not an environment variable. Skill references name packaged workflows, not a Claude Skill tool. Read references/codex/delegation.md before any specialist handoff; role names are procedures, not installed agent profiles.

Read and apply [Client communication](../../references/client-communication.md) completely.
Read [Request publish](../../references/changes/request-publish.md) completely and follow it.
Resolve scripts against `<plugin-root>/scripts/`.
Preview and confirm the review PR. Never merge it or deploy the application.
If changes need submitting first, use `$abacus-submit` with its own review.
