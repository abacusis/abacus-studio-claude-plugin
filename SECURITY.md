# Security and access

This repository distributes the Abacus Studio plugin only. It contains no client
application source, authorized app list, saved credentials, or database contents.
Public service URLs and the Studio Supabase project reference identify the
service; they do not grant access. Studio validates authentication, membership,
local-development enablement, and the assigned client repository server-side.

## Credentials

- OAuth uses PKCE and a loopback callback. Tokens remain in supported OS storage:
  macOS Keychain, Windows Credential Manager, or Linux Secret Service.
- Git credentials are obtained privately for the assigned repository. They are
  not stored in the remote URL or printed in the normal command workflow.
- Repository credentials grant repository access, not branch-only isolation.
  Use a separate private client repository and appropriate GitHub rules.
- Sandbox app keys can be written to an ignored local `.env`. Local users and
  coding tools can read them. A sandbox server secret bypasses sandbox RLS;
  sandbox isolation does not make disclosure harmless.
- Supabase management tokens stay in Studio. Never configure production keys.
- Disconnect does not delete local `.env` keys or independently installed legacy
  connectors. Revoke or rotate keys separately when access ends.

## Execution and review

Setup requires approval of the destination and local commands. Dependency scripts
and application code execute locally, so inspect them and use trusted repositories.
Studio-selected skill packages are pinned and checksum-verified; installation
does not run upstream installers or enable hooks. A skill's own launcher may
download an executable when invoked, subject to the coding tool's permissions.

Submission fetches before synchronization and push, requires reviewed checks, and
does not force-push. Publishing requests a PR; it does not merge or deploy.
Deployment automation attached to the repository must be reviewed separately.
Secret scanning is best-effort, not proof that a patch is free of sensitive data.
Legacy snapshot/sync helpers are retained for compatibility but are not exposed
as client commands and are not used by the normal Git setup/submit workflow.

## Report a concern

Report security issues privately through Abacus Studio Support. Do not include
credentials, customer data, or private application source in public GitHub issues.

The release audit is a bounded source/package review, not a penetration test or
a certification of the Studio backend. Windows and Linux end-to-end validation
is still required before claiming broad platform support.
