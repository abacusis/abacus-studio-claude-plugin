---
name: abacus-connect
description: Sign in to Abacus Studio or renew your authorization.
---

Resolve `<plugin-root>` from the absolute source path of this loaded skill: two directories above its directory. Substitute that real path in commands; it is not an environment variable. Skill references name packaged workflows, not a Claude Skill tool. Read references/codex/delegation.md before any specialist handoff; role names are procedures, not installed agent profiles.

Read and apply [Client communication](../../references/client-communication.md) completely.
Read [Connect](../../references/workspace/connect.md) completely and follow it.
Use the current user request as the input.
Resolve scripts against `<plugin-root>/scripts/`. Treat app names as
search data. Connect does not approve setup, submitting, or publishing.
Offer `$abacus-setup` when the user wants a local preview.
