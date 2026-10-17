---
name: request-publish
description: Send your sandbox changes for publishing review.
disable-model-invocation: true
---

Read and apply [Client communication](../../references/client-communication.md) completely.
Read [Request publish](../../references/changes/request-publish.md) completely and follow it.
Resolve scripts against `${CLAUDE_PLUGIN_ROOT}/scripts/`.
Preview and review the PR; the user's request authorizes opening it. Do not ask
again about routine wording. Never merge or deploy. For “submit and publish,”
use `/abacus-studio:submit` first under the same request. Request publish alone
does not authorize saving local edits.
