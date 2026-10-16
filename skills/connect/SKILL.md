---
name: connect
description: Sign in to Abacus Studio or renew your authorization.
disable-model-invocation: true
argument-hint: "[optional app name]"
---

Read and apply [Client communication](../../references/client-communication.md) completely.
Read [Connect](../../references/workspace/connect.md) completely and follow it.
The request is: $ARGUMENTS
Resolve scripts against `${CLAUDE_PLUGIN_ROOT}/scripts/`. Treat app names as
search data. Connect does not approve setup, submitting, or publishing.
Offer `/abacus-studio:setup` when the user wants a local preview.
