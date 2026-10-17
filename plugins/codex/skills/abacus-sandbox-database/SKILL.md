---
name: abacus-sandbox-database
description: Use when a Studio-connected app needs a sandbox schema migration, including missing tables or columns and features requiring database changes.
---

Resolve `<plugin-root>` from the absolute source path of this loaded skill: two directories above its directory. Substitute that real path in commands; it is not an environment variable. Skill references name packaged workflows, not a Claude Skill tool. Read references/codex/delegation.md before any specialist handoff; use approved project-scoped Abacus profiles when available.

This is an internal development capability, not a client menu command.
Read and apply [Client communication](../../references/client-communication.md) completely.
Read [Sandbox migrations](../../references/changes/migrate.md) completely before
acting. Resolve scripts against `<plugin-root>/scripts/`.
Prepare new migration files in the selected client repository. Studio needs
committed, submitted sandbox migrations; use the reviewed Submit workflow
when the user authorizes submission. Then preview the migration through Studio,
explain it, obtain approval for the exact SQL, and apply with the reviewed ID.
Do not ask the client to remember or run a migration command. Preserve all
approval and sandbox boundaries. This does not authorize production changes
or function deployment.
