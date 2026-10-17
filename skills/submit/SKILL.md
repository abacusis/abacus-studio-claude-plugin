---
name: submit
description: Review your changes and save them to the sandbox repository.
disable-model-invocation: true
---

Read and apply [Client communication](../../references/client-communication.md) completely.
Read [Submit](../../references/changes/submit.md) completely and follow it.
Resolve scripts against `${CLAUDE_PLUGIN_ROOT}/scripts/`.
Preserve fetch-first, diff review, conflict resolution and checks. The user's
Submit request authorizes normal commit/check/push steps; do not re-ask approval.
For “submit and publish,” continue to `/abacus-studio:request-publish` under the
same request. Submit alone does not authorize opening a review PR.
