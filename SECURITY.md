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

The plugin includes a routing-only UserPromptSubmit hook. It executes a small
local Python script that returns constant guidance to select the appropriate
workflow. It does not read prompt input, files, tokens, or transcripts, and does
not upload data, modify projects, launch agents, or approve actions. It has a
five-second timeout and command failure is non-blocking. Disabling hooks may
reduce automatic routing reliability; no permission bypass is attempted.

Separate dashboard observers run only after workspace opt-in. They select lifecycle
IDs, tool names and filtered file paths from hook input, storing local metadata in
the Git-ignored `.studio/dashboard` directory. Pre-action callbacks expose only the
action category and filtered Read/Edit/Write paths—not command text or search
patterns. Observers discard prompts, transcripts,
tool bodies/output and agent responses. Coordinator-written summaries must contain
no sensitive information; filtering is not comprehensive secret redaction.
The optional server binds only to loopback with an unguessable URL, Host/Origin
checks and no external assets. Keep that URL private. Buttons queue two fixed
workflow requests, consumed on the next Claude prompt; they cannot run arbitrary
commands or grant approval. Local users can read local metadata. Tracking can be
disabled without deleting history; stop the server separately using its helper.

Setup requires approval of the destination and local commands. Dependency scripts
and application code execute locally, so inspect them and use trusted repositories.
Studio-selected skill packages are pinned and checksum-verified; installation
does not run upstream installers or enable hooks. A skill's own launcher may
download an executable when invoked, subject to the coding tool's permissions.

The Builder has editing and shell tools, constrained by host permissions and the
coordinator's approved scope; prompt instructions are not a filesystem sandbox.
Its work is not independent verification or publishing authorization.

The Verification Specialist has no Edit/Write tools, but approved test commands
can still have side effects through Bash. Its instructions prohibit application
edits and unapproved data writes; host permissions remain the execution boundary.
A separate agent is not human approval or a security certification.

The Code Reviewer has only Read, Grep, and Glob tools: no shell or file editing.
The UI Reviewer uses those reading tools to inspect approved local screenshots;
it cannot capture images, browse, run scripts, or edit the app. Screenshots may
contain sensitive information and reading them can send pixels to the AI provider.
No screenshot inspection implies full accessibility, UX, or publishing approval.
The UX Reviewer also has only Read/Grep/Glob. It reviews approved source, images,
and interaction evidence; it cannot submit forms, operate browsers, run scripts,
or change data. Actual actions remain with the coordinator or authorized verifier,
under existing sandbox/write approval. Evidence review is not an independent run.
The Readiness Reviewer also has only reading tools. It reconciles supplied checks
and findings but cannot waive required evidence, run tests, fix source, or approve
publishing. It is guidance, not an enforced deployment gate or proof of evidence
authenticity; Abacus review and publication authorization remain separate.
The Security Reviewer uses the same restricted tool list for source-only analysis;
it cannot run attacks or tests, probe services, or remediate findings. Source-only
candidates stay Needs validation without severity unless independent evidence
establishes the complete failure and actual result. It is not a pen test.
It performs source inspection within the authorized workspace and returns findings
to the coordinator, not fixes or publishing approval. Reading tools still require
host access controls; the agent is instructed not to read credentials or unrelated
customer data. Its source review is not a penetration test or security certification.

Optional local browser verification installs pinned Python Playwright and Chromium
only with approval, separately from the app. It uses a fresh browser context, not
personal profiles or imported sessions. Managed captures require a current Studio
workspace, approved loopback target, and reviewed action scope. External HTTP
origins and writes are blocked unless separately approved; WebSockets and service
workers are blocked. Browser filtering cannot prevent a local server from reaching
production or performing effects on GET, so verify sandbox backing before capture.
Screenshots stay in Git-ignored local evidence and can contain sensitive data.
Viewing them in an AI tool may transmit them to that tool's provider. No automatic
redaction, login, video, trace, or Studio upload is provided. Capture is not a pass;
image inspection and criterion-linked assertions are separate evidence.

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
