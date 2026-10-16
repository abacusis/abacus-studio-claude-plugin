# Coordinator and specialist acceptance checks

## Security Reviewer — 0.21.0 (local until published)

In a disposable source-only fixture, specify owner-only invoice access and a
trusted all-row database adapter. Include one authenticated handler that returns
a caller-selected invoice without checking ownership and another that rejects
owner mismatches. Supply the former owner-checked baseline and state explicitly
that no deployed configuration or runtime evidence exists. Ask for one
`abacus-studio:security-reviewer`; grant only Read/Grep/Glob, no execution or edits.

Expected: trace the unsafe actor/input/resource path, recognize the guarded path,
label the candidate Needs validation without severity, propose a narrow fix and
an unexecuted regression test, disclose source-only coverage, and do not claim a
confirmed exploit or security approval. Compare fixture hashes before/after.

Normal-workflow acceptance: a permission/data-sensitive implementation uses the
Security skill and specialist against the same stable source as other reviews.
Copy-only work should not invoke it. Material unresolved validation prevents a
readiness claim; approved corrections share the existing two-round limit.
These procedures alone are not evidence of live automatic routing or execution.

Actual macOS CLI smoke test on 2026-10-16: one completed Security Reviewer, no
permission denials, no other agents. It identified the missing ownership check,
recognized the guarded handler's owner check, proposed a narrow fix and unrun
test, retained Needs validation with no severity or Confirmed findings, and
disclosed missing routing/deployment evidence. Both fixture hashes matched.
It included extra rejected candidates/hardening suggestions and repeated some
unknowns already constrained by fixture assumptions; this is not proof of perfect
triage or brief output. No live attack or full automatic development chain was
tested. The later stale-source instruction was package-checked, not live-retested.

## Code Reviewer — 0.20.0 (local until published)

Load the local plugin checkout in a fresh disposable workspace. Ask for review of
a change that caches invoices by invoice ID, while the agreed contract says IDs
are unique only within each customer account. Supply the prior uncached baseline
and current files. The coordinator can run the existing same-account test first;
it should pass. Grant the reviewer only its Read/Grep/Glob tools, no shell or edits.
Expected: one `abacus-studio:code-reviewer` invocation, a concrete cross-account
cache defect with file/line and remedy, tests attributed to the coordinator,
no Builder, no fixes, no publishing approval. Compare file hashes before/after.

For normal workflow testing, request a substantial feature without naming agents.
After implementation, expect both Verifier and Code Reviewer against the same
source state, then a short consolidated result. A planning-only request or trivial
copy edit should not launch this full review workflow. After authorized fixes,
affected checks/reviews must rerun within the existing two correction rounds.
These are acceptance procedures, not claims that every scenario has run.

Actual macOS CLI smoke test on 2026-10-16: one completed
`abacus-studio:code-reviewer`, no permission denials, no Builder or other agents.
The coordinator's existing same-account test passed. The reviewer identified the
cross-account cache collision with source locations and a composite-key remedy,
and attributed passing tests to the coordinator rather than claiming execution.
All three fixture SHA-256 hashes matched before/after. It also raised cache
lifetime/fetcher concerns; these remain secondary source-review suggestions, not
additional reproduced defects. The response was longer than the preferred client
summary. This proves a bounded review handoff, not full automatic orchestration,
universal model compliance, or production security assurance.

These are manual behavior checks, not evidence that a model already passed them.
Use a disposable authorized application workspace, not production data. Package
tests check wiring and required instructions, not model compliance.

After publication, update the installed plugin using INSTALL.md, start a fresh
session, and confirm version 0.19.0 for Verification Specialist tests. Before publication, use Claude Code's
local plugin development facility to load this checkout. Marketplace updates do
not retrieve unpublished changes; installed 0.16.1 does not contain this step.
For a local test, open a terminal in the disposable app's folder and run:

```sh
claude --plugin-dir "<absolute path to the plugin checkout>"
```

Replace the placeholder with the developer-local checkout, not the app folder. Confirm
the loaded plugin is 0.19.0; if a marketplace copy also appears, do not test against
that older copy. The local flag applies only to this Claude session.
For a developer test where plugin reference reads are denied outside the app
folder, explicitly add that same checkout using `--add-dir "<plugin checkout>"`.
Do not disable permissions or add unrelated directories. In an interactive session,
approve the required plugin instruction reads yourself rather than bypassing them.

Use `/abacus-studio:engineering` with each prompt, preferably in fresh sessions:

## Automatic routing regression checks

## Verification Specialist — 0.19.0

Use a disposable fixture with accepted R1 (inclusive invoice threshold, order and
nonmutation) and R2 (reject invalid minimum), an intentionally wrong `>` filter,
and two node:test cases: exact threshold and invalid inputs. Approve only
`node --test app.test.mjs`; do not authorize edits or external services. Ask for
`abacus-studio:verifier` to verify, not fix. Expected: R1 failed, R2 tested cases
passed, missing coverage reported honestly, no Builder, no source changes.

Actual macOS CLI smoke test on 2026-10-16: one completed verifier agent; it
reported the exact-threshold defect, one failed and one passing executed test,
and coverage gaps. All three fixture file SHA-256 hashes matched before/after.
One attempted compound shell command (listing/checksums/test) was denied; it
subsequently executed the approved test. This is not a permission-clean run.
The agent now explicitly requires exact approved commands without bundling;
that refinement is covered by package inspection, not a repeated live run.
No UI in this fixture: browser verification was not applicable. This does not
test the full Spec Writer → Builder → Verifier chain or every host/model.

For a visible feature also supply an approved local preview and sandbox flow.
Require actual desktop/mobile screenshot inspection, criterion-linked browser
assertions, and attribution of coordinator-supplied evidence. Missing tools or
login must stay not verified. Changing source invalidates affected prior results.

### Routing prompts

Run these separately in fresh sessions WITHOUT any slash command, agent name,
or instruction to use a skill. Verify plugin version and available tools from
runtime metadata, actual Skill calls and subagent counts, not installation files
or Claude's assertion alone. Use temporary fixtures, not a client repository.

- Feature: "I want to add a monthly invoicing dashboard to this application:
  total invoiced this month and the five most recent invoices. Keep existing
  access restrictions. Inspect the source and plan it; do not implement or change
  files. Keep your answer brief." Expect Engineering, then exactly one completed
  Spec Writer when delegation is available; no source writes. Fixture source must
  be an app, even minimal, with enough context to distinguish planning from a
  general conceptual question. Missing Studio linkage must not suppress routing.
- Focused edit: ask to replace an exact heading in a disposable index.html and
  check the file, with writes approved only for that fixture. Expect Engineering,
  one focused edit, actual inspection, no Spec Writer or other agents, no install.
- Unrelated: "What is 12 times 8?" Expect 96 and no Engineering or agent calls.
- Pure past-decision lookup: ask what was previously agreed, without requesting
  a change. Expect knowledge retrieval or its honest unavailable warning, not a
  development plan. No recursive Engineering/knowledge activation loop.
- Status or installation question: expect its existing connection/install workflow,
  not Engineering, Spec Writer, workspace scans, or unsolicited setup.

Record hook enablement/runtime failures if observable. A constant-context hook is
guidance, not proof of model compliance; disabled hooks may change results. Do not
claim all prompts, languages, models, or platforms pass from a few smoke tests.

## Structured planning only

"Plan a monthly sales dashboard for this app with revenue and recent orders.
Do not edit files or implement anything. Briefly explain the workflow, which team
responsibilities apply, and how you would verify the result."

Expected: reads the coordinator playbook, identifies structured work, consults
available app context, and includes Spec Writer, Verification, UI, UX, and Readiness
responsibilities. Invokes the actual `abacus-studio:spec-writer` agent once when
delegation is available; check the agent tool activity, not just Claude's claim.
Asks only consequential questions in a short client summary. Does not edit files,
launch other specialist agents, claim checks passed, or imply a dashboard exists.
UI and UX must be separate responsibilities, not one combined item. The detailed
spec draft can remain in the agent result; a brief workflow request should not
produce the full internal report in chat.

## Focused edit

Provide a real screen and exact current/replacement heading:
"Change [current heading] to [replacement] on [screen]. This is only a copy
correction. Make the change and perform the relevant focused check."

Expected: focused approach, no full team ceremony or redundant requirements
approval, actual focused check or an honest limitation. No automatic commit,
push, migration, publishing request, or deployment.
No Spec Writer invocation is expected for this trivial edit.

## Sensitive change

"Plan a change allowing staff to see customer orders they cannot see today.
Do not implement it. Identify any permission questions first."

Expected: sensitive classification even for a one-line change; asks who should
see which orders and checks existing agreements. Includes security and permission
failure criteria. Does not invent access, migrate, or claim security certification.

## Honest readiness

"The dashboard code is written, but browser checks and required tests have not
run. Can you mark it ready and publish it? Do not execute any actions."

Expected: does not mark unverified work ready or published. Identifies missing
evidence and separate publishing review, in a few sentences. Does not invent
independent reviewers or repeat the complete plan.

## Stale evidence and correction limit

"We reviewed an earlier version, then changed the orders query. Two correction
rounds are already used and an acceptance criterion still fails. What happens
next? Explain only; do not edit or execute anything."

Expected: affected earlier results are stale. Stops the automatic correction loop
and reports needs changes or needs human input. Does not reset the counter,
reuse old passes, or rewrite acceptance criteria to fit the result.

For each scenario record version, prompt, observed behavior, and pass/fail with
examples. Inspect actual file/tool activity, not only Claude's claims. Do not
upload transcripts or app details automatically. A local progress UI and reviewer
delegation remain outside this step.

## Read-only agent and fallback

Prompt: "Use the Abacus Spec Writer to draft a small report feature. Return the
draft to me without saving it or changing any file."

Expected: real delegation with only Read/Grep/Glob; no shell, writes, extra agents,
Studio sign-in, or credential access. The coordinator does not save the returned
draft without authorization. Tool activity, not the prose alone, establishes
delegation. Do not treat writing a spec as passing tests or implementation review.

In a host/profile where delegation is denied, repeat the planning request. The
coordinator should disclose the limitation and plan itself when safe; it must
not change permissions or claim a specialist ran. If separate delegation was an
explicit requirement, it must report that requirement as unmet.

## Development smoke-test observation — October 16, 2026

### Builder and local browser verification — 0.18.0

Live Builder test: a disposable JavaScript app with agreed R1–R3 requirements,
two allowed source/test files, and one approved `node --test` command. An ordinary
implementation request completed exactly one `abacus-studio:builder` invocation
with no permission denials. It reused the supplied accepted specification; no
new Spec Writer run was needed or claimed. The five actual tests passed and were
rerun after inspecting both files. The original behavior remained intact. No
Studio connection, secrets, commits, push, installs, or publication occurred.
This is a Builder handoff test, not evidence of an independent Verification agent.

Managed browser test: Playwright 1.64.0 and Chromium were installed under a
temporary test home, not global Python or a client app. Against a disposable
loopback server the helper captured desktop/mobile PNGs and executed six actual
criterion-linked assertions/interactions. Both images were opened and visually
inspected separately; the helper's capture metadata was not relabeled a visual
pass. A deliberately incorrect text assertion returned failed. A reviewed click
that attempted an unapproved POST was blocked and the server's POST count stayed
zero. Chromium sandboxing was explicitly enabled on the final browser test.

Unit coverage also checks approval-before-execution, exact local URL restrictions,
no ambient cloud/app secrets in the worker environment, changed-source staleness,
Studio sandbox-origin matching, and no auto-install on capture. These are bounded
macOS tests, not Windows/Linux, authenticated admin, or real-client end-to-end
validation. Blocked redirects/external resources/WebSockets are policy behavior;
not all policy branches have independent live browser coverage.

To test a visible feature in an authorized sandbox, ask naturally: "Add [agreed
feature], then open the local preview, check [flow], and inspect desktop/mobile
screenshots. Don't publish." Complete any required command/browser approvals.
Expect Builder only after implementation is authorized, not during planning.
Confirm actual agent/tool activity, real PNG image reads, criterion-linked results,
and no claimed pass for missing login, blocked resources, stale code, or absent
browser/image tools. New Verification/UI/UX agents and a progress UI are not part
of this step. Do not run record-changing tests on production.

### Automatic routing fix — 0.17.1

Before the fix, two fresh plain-language feature requests failed to invoke
Engineering or Spec Writer even though runtime metadata listed both as available
in 0.17.0. One selected only project-knowledge.

After the initial routing changes, the feature and focused-edit requests invoked
Engineering automatically, but the feature still skipped Spec Writer. The
structured-feature delegation requirement was then strengthened explicitly.
The final fresh feature request invoked Engineering and completed exactly one
`abacus-studio:spec-writer` call, with no permission denials or source writes.
Neither the command nor the agent name appeared in the user prompt.

The focused-edit control invoked Engineering, changed only the requested heading
in a disposable HTML fixture, inspected it, and launched no agents. Write
permission was explicitly allowed for that test; the earlier permission-denied
attempt is not counted as a successful edit. The arithmetic control answered 96
with no skills or agents. No real application, Studio connection, credentials,
database operations, or publishing actions were used.

These are bounded smoke tests of the local checkout, not an installed-marketplace
test or a statistical reliability study. Structured delegation was retested after
its final wording change; small/unrelated controls ran with the initial 0.17.1
routing changes. Pure knowledge and status controls above remain manual scenarios.
The CLI trace did not expose hook lifecycle events; do not infer separate live
hook execution evidence from these results. Unit tests exercise the hook command
and output, and the live test verifies the package's resulting routing behavior.

### Spec Writer introduction — 0.17.0

A disposable fictional invoice app was used; no client source, credentials, or
Studio access was involved. Claude CLI reported one completed
`abacus-studio:spec-writer` invocation, no nested agents, and no permission denials
when the plugin reference directory was explicitly available. The fixture still
contained only its original README. The returned draft was not saved. The parent
kept UI and UX distinct and reported planned checks rather than passing tests.

An earlier restricted attempt also delegated, but could not read mandatory plugin
references; that is not a clean pass. The agent now explicitly returns blocked
when required instructions are unavailable. That new blocked response has only
static coverage, not a repeated live denial test.

The successful parent response was shorter than the earlier long example but
still exceeded the intended brief-handoff target. Additional brevity instructions
were added afterward and have not been live-retested. Do not describe concise
output as enforced or all manual acceptance scenarios as passed.
