# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

User approved lightweight HTML/CSS/JavaScript served by the plugin's existing
Python runtime for the local progress dashboard. No new app framework required.

## Users

Clients building their applications in Claude Code with the Abacus Studio plugin.
They want to understand what the AI specialists are doing without reading long
technical conversations. Abacus engineers also need accurate evidence and gaps.

## Product Purpose

Make local AI development understandable: who is working, the current stage,
review findings, checks still missing, and what is local versus saved to GitHub.

## Operating Context

The plugin runs in a local Claude session. The main conversation coordinates eight
specialists: Spec Writer, Builder, Verification Specialist, Code Reviewer, Security
Reviewer, UI Reviewer, UX Reviewer and Readiness Reviewer. The approved dashboard
is local, not a Studio worker or a publishing console. Its two action buttons
queue requests for Claude's existing workflows, never execute Git or publishing.

## Capabilities and Constraints

Step 10 implementation is approved, with visual mockup approval before interface
code. User confirmed a dark high-tech control-room style and mockup-first workflow.
Show real activity, never simulated agent execution. Local working-tree changes,
unpushed commits, remote-tracking freshness and unknown access need distinct labels.
Do not imply that locally cached remote-tracking refs prove current GitHub state.
No automatic fetch, push, publishing, Studio progress upload, or new credentials.
Disconnected or stale activity must not look like active ongoing work. Exact local
storage and lifecycle instrumentation remain engineering decisions to validate.

## Evidence on Hand

The plugin has working specialist definitions and documented bounded smoke tests.
No dashboard exists yet. Mockup agent activity and file counts must be labeled
illustrative, not screenshots of running agents or real project records.

## Product Principles

- Recorded evidence over reassuring animations or invented progress percentages.
- Show the team and next action in plain language.
- Saving to a sandbox repository is different from publication.
- Never turn a local observer into unattended execution or elevated access.
