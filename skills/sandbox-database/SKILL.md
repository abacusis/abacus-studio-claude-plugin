---
name: sandbox-database
description: Use when a Studio-connected app needs a sandbox schema migration, including missing tables or columns and features requiring database changes.
user-invocable: false
---

This is an internal development capability, not a client menu command.
Read [Sandbox migrations](../../references/changes/migrate.md) completely before
acting. Resolve scripts against `${CLAUDE_PLUGIN_ROOT}/scripts/`.
Prepare new migration files in the selected client repository. Studio needs
committed, submitted sandbox migrations; use the reviewed Submit workflow
when the user authorizes submission. Then preview the migration through Studio,
explain it, obtain approval for the exact SQL, and apply with the reviewed ID.
Do not ask the client to remember or run a migration command. Preserve all
approval and sandbox boundaries. This does not authorize production changes
or function deployment.
