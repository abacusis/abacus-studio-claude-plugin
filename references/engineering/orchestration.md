# Coordinate the development workflow — Steps 1 through 6

The main Claude Code conversation is the local coordinator. Read this playbook
before planning or implementing an application change through Engineering.
Use existing project knowledge, code mapping, and relevant playbooks; do not
replace them with a second planning system.

## Current capability boundary

The coordinator remains the main conversation. Five specialist agents are installed:
`abacus-studio:spec-writer` with read-only tools and `abacus-studio:builder` with
scoped development tools subject to host permissions, plus `abacus-studio:verifier`
for evidence-based checking without application edits, and read-only
`abacus-studio:code-reviewer` for engineering review, plus read-only
`abacus-studio:security-reviewer` for security boundaries. Delegate structured or
sensitive specification work to it when the host allows delegation. This is
required even for planning-only features; do not silently substitute your own
draft while that agent and delegation tool are available. The host may expose
delegation as Task or Agent. A small codebase alone is not a fallback reason. Other
specialist agents, quality-check hooks, a local progress UI, durable run state, and Studio
progress synchronization are NOT implemented. Do not spawn specialist reviewers
that are not installed, simulate separate conversations, or claim they ran.
Builder performs authorized structured implementation; the coordinator still
owns review, readiness, and client decisions. Separate specification drafting
or builder-reported tests are not independent implementation verification.
Version 0.17.1 adds a routing-only UserPromptSubmit hook to remind the main
conversation to load Engineering for development requests. It does not execute
the workflow, enforce model compliance, or change any permission boundary.

### Spec Writer handoff

Before delegating, retrieve relevant Studio knowledge when the app is configured.
Send the feature request, authorized workspace, existing spec/version if any,
confirmed requirements, relevant source pointers, knowledge excerpts with source
and approval metadata, unavailable-context warnings, exclusions, and planning-only
or implementation authorization. Do not send credentials, full transcripts, or
unrelated customer data. Pass actual needed context, not just a link the agent
cannot retrieve with its read-only tools.

Invoke the installed namespaced `abacus-studio:spec-writer` agent; inherit the
client's model rather than choosing a different paid model. Wait for its result
before implementing dependent behavior. The agent returns a draft; the coordinator
checks it against the request and existing agreements, asks material questions,
and saves a document only under the existing artifact-placement approval rules.
Do not paste the agent's full draft into chat by default. Give a short summary
and only the next blocking questions, generally up to three. Keep optional later
choices and the full draft in the handoff or authorized artifact. A brief workflow
request should normally fit within about 150 words, unless material approvals or
evidence require more. Keep UI and UX separately labeled when they are requested.
For this brief handoff, prefer one outcome sentence, up to three short questions,
one short UI line and one short UX line if requested, and a single next action.
Avoid restating the feature, blockers, and "nothing built" more than once.
Spec Writer cannot save files or approve its own draft. Clear authorized requests
can proceed without another ritual approval pause.

Do not delegate for trivial edits, connection/status, or questions about the
plugin's own workflow. Do not repeatedly spawn/resume the agent to evade its
20-turn limit; report partial results and clarify the next scoped step.
If unavailable or denied, say so briefly and plan in the main conversation when
safe. Do not retry permissions, create an unrestricted substitute agent, change
the model, or claim delegation occurred. An explicit user requirement for separate
delegation remains unmet until it actually runs. Report failures honestly.

Execution depends on the local Claude session. Do not promise continued work
after disconnection or automatic recovery. Use actual project files and confirmed
conversation context when continuing; recheck the source and invalidate affected
verification after edits. Do not invent a saved job or recovery capability.

## 1. Choose a proportionate approach

Classify by consequences, not file count. A one-line permission or payment change
is sensitive, not small. When uncertain, investigate the impact before classifying.

| Approach | Examples | Work required |
| --- | --- | --- |
| Focused | Correct text or isolated spacing with no behavioral/access change | Implement the authorized edit and perform a relevant focused check. No full team ceremony. |
| Structured | Add a screen, feature, or business workflow | Requirements and acceptance criteria, implementation, verification, relevant reviews, and readiness assessment. |
| Sensitive | Change permissions, payments, privileged access, customer-data exposure, or shared-data behavior | Structured workflow plus explicit permission/failure criteria and relevant security review. |

Explain the approach in one or two plain-language sentences, not a long internal
process report. No mandatory classification questionnaire or model-selection step.

## 2. Establish the expected result without unnecessary pauses

Read available application decisions and inspect current behavior. For a clear,
authorized implementation request, summarize the scope and proceed. Existing
confirmed requirements do not need another approval just because this playbook ran.

Ask when an unanswered question materially changes behavior, scope, consequences,
or a current approved agreement. Do not invent an answer. A planning-only request
stays planning-only. Plan approval alone is not implementation authorization.
Separate host execution, migration, conflict resolution, push, and publishing
approvals remain required by their existing workflows.

For substantial changes, follow the specification playbook for stable requirement
IDs, acceptance criteria, exclusions, and artifact placement. Keep small plans in
chat when sufficient. Never rewrite an accepted requirement to fit the result.

## 3. Map responsibilities to this change

Only Spec Writer, Builder, Verification Specialist, Code Reviewer, and Security Reviewer are installed specialist agents. The remaining roles
are responsibility areas performed by the coordinator, not installed agents.
Do not claim independent reviewer execution or launch the whole roster for a
focused edit.

| Role | Responsibility | When relevant |
| --- | --- | --- |
| Orchestrator | Keep scope, stages, findings, and next action consistent. | Every application change. |
| Spec Writer | Clarify behavior, acceptance criteria, and exclusions. | Structured and sensitive changes. |
| Builder | Implement the agreed behavior and relevant tests. | Authorized implementation. |
| Verification Specialist | Match criteria to actual checks, results, and gaps. | Structured and sensitive changes; focused checks for small edits. |
| Code Reviewer | Check correctness, architecture, maintainability, and regressions. | Structured and sensitive changes. |
| Security Reviewer | Examine relevant source-level access and data boundaries. | Security-sensitive changes; source-only Security limits apply. |
| UI Reviewer | Check visual consistency, spacing, hierarchy, responsive layout, and presentation. | Changed visible interfaces. |
| UX Reviewer | Check user flows, navigation, feedback, accessibility, and loading/error/empty states. | Changed interaction or workflow, including accessibility effects. |
| Readiness Reviewer | Compare the agreed result, checks, and unresolved findings. | Structured and sensitive changes. |

Keep UI and UX as separate named responsibilities in plans and review summaries;
never collapse them into a single "UI/UX review" item. If both are inapplicable,
omit them from the short client update rather than reciting the whole roster.
UI asks whether the interface is presented
well; UX asks whether people can complete the intended task. Neither substitutes
for browser evidence or an accessibility check that has not actually occurred.
Use the existing Design capability when relevant, within its authorization.

## 4. Build, verify, and review the actual result

When implementation is authorized for a structured/sensitive change, invoke
`abacus-studio:builder` with accepted requirements/spec version, the authorized
workspace, relevant context, allowed files and commands, current edits, and
preview/browser approval scope. A Spec Writer draft alone is not authorization
to implement. No Builder for planning-only work or a trivial text correction.
Wait for the result before reviewing; do not edit the same files concurrently.
The Builder may return implemented, partial, or blocked. Inspect the actual diff
and executed-check evidence rather than accepting the status as proof.

Do not silently substitute implementation in the main conversation while Builder
is available. For actual unavailability, denial, or failure, disclose the gap and
continue only within the user's scope; an explicit separate-agent requirement
remains unmet. Do not spawn replacements to evade the 40-turn budget or claim
another agent ran. Further correction uses the existing maximum two rounds.

Visible changes need [local browser verification](browser-verification.md): a
current approved preview, relevant assertions/flows, desktop/mobile screenshots,
and actual image inspection. Use host tools or the separately approved fallback;
missing browser/authentication/image support stays not verified, not a pass.

After structured/sensitive implementation, invoke `abacus-studio:verifier` with the
accepted spec/version and criterion IDs, workspace, current source identity and
local edits, relevant diff/test pointers, approved commands, and preview/browser
approval. Wait for its result. Do not edit relevant files concurrently. The verifier
reads source/tests and runs approved checks itself; Builder-only reports are not
verification passes. Host-browser checks supplied by the coordinator must retain
that provenance. Do not send secrets or assume authentication is available.

The verifier cannot fix source/tests, waive criteria, or approve publishing. Route
defects to Builder within at most two correction rounds; rerun affected verification
against the changed source. Unavailable/denied/failed delegation must be disclosed;
coordinator checks are a fallback, not a separately executed verification. Its
verified status covers only evidenced criteria, not readiness or security certification.

For substantial structured/sensitive implementation also invoke the installed
`abacus-studio:code-reviewer` with authorized workspace, accepted scope/spec,
comparison baseline or diff, current source including local edits, conventions,
and verification evidence with provenance. It reads source and callers but cannot
edit, run tests, or approve publication. Missing baseline means a limited source
review, not a claimed complete diff review. Relevant explicit review-only requests
can use this agent without invoking Builder or manufacturing a new specification.

Code Reviewer and Verifier may run in parallel against the same stable source;
wait for both before readiness and never edit reviewed files concurrently.
Consolidate concrete findings separately from optional suggestions; do not count
two agents agreeing as proof. Send authorized fixes to Builder within the existing
two-round limit and rerun affected verification/review. Disclose actual unavailable,
denied, or failed delegation; coordinator review is not a separate-agent review.

For security-sensitive changes use the Security skill and installed
`abacus-studio:security-reviewer`. Supply authorized paths, intended access rules,
baseline/diff, source identity including local edits, and evidence provenance.
Review relevant permissions, tenant data, payments/webhooks, injection, secrets,
uploads, and AI/tool boundaries—not every category for every change. No extra
security ceremony for trivial nonsensitive edits.

Security review may run alongside other checks against stable source. It cannot
execute code, probe services, edit files, or spawn agents. Wait for relevant results
before readiness. Preserve Needs validation without severity when actual outcome
or independent evidence is missing; agent agreement does not confirm an exploit.
Material unresolved security validation prevents claiming ready to preview.
Consolidate duplicate findings and route authorized fixes within the same two
correction rounds, then rerun affected reviews. Disclose unavailable/denied/failed
delegation; never represent it as an agent review or clean security pass.

Use a short working outline: understand/specify, build, verify/review, resolve,
assess readiness. Label stages planned, in progress, completed, blocked, or not
applicable with a reason. Chat progress is not a dashboard or durable job record.

Review the same identified source state and accepted specification. Use the
available Git revision plus the relevant uncommitted/untracked changes; HEAD
alone does not identify an edited working tree. Do not commit just to label it.
After edits, rerun affected checks and revisit affected reviews. Never reuse a
passing result for changed code without explaining why the check remains valid.

For each acceptance criterion record:
- Criterion ID and the agreed behavior/version.
- Source state checked (including local edits where relevant).
- Actual command, browser action, manual observation, or source inspection.
- Result: passed, failed, blocked, or not verified.
- Evidence, limitations, and who/what reported the result.

Keep planned tests distinct from executed checks. Source inspection does not
count as a passing runtime test. Do not claim independent verification when the
same conversation built and reviewed the change. Never manufacture screenshots,
test output, reviewer agreement, passing coverage, or human confirmation.

## 5. Resolve findings with a bounded loop

Consolidate relevant findings, remove duplicates, and prioritize demonstrated
defects. Fix within the authorized implementation scope; a review-only request
does not authorize fixes. Explain disagreements instead of using majority vote.
Preserve existing conflict-resolution and database approval requirements.

Allow at most two correction rounds after the initial implementation/review.
Recheck affected criteria and review lenses after each round. If a material issue
remains, stop and report the blocker rather than extending the loop automatically.
Further work needs a new scoped user direction; do not reset the round counter
silently or change acceptance criteria to obtain a pass.

## 6. State readiness without granting approval

Return one of these outcomes for structured/sensitive work:
- Ready to preview: required checks and relevant reviews are complete for the
  current source, with no unresolved blocking findings. Explain any remaining
  non-blocking limitations and which checks were separately executed versus supplied.
- Needs changes: a demonstrated unmet criterion or defect remains. Explain what
  needs correcting; stop after the correction limit.
- Needs human input: a material decision, missing access, required manual check,
  unavailable verification, or unresolved review disagreement prevents readiness.

The Readiness Reviewer is not a publishing Approver. Ready to preview is not
independent verification, Abacus approval, a security certification, saved to the
sandbox repository, or approved to publish. Never merge or deploy based on it.

Finish briefly: what changed, what was actually checked, what remains, and the
next useful action. For focused edits, a concise result and relevant check is
enough; do not generate a full review report. Keep required evidence accessible
in the agreed artifact or provide it when the client asks. Saving and publishing
remain the explicit Submit and Request publish workflows. This playbook adds no
commands, permissions, automatic commits, pushes, migrations, or uploads.
