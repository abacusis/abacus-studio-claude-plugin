# Choose depth before choosing agents

Read this short routing guide first. User preference + actual complexity +
potential consequences determine the work. No extra command or questionnaire.
This is model guidance, not a deterministic classifier or permission mechanism.

## Understand the current request

Infer preference from the user's own words and conversation, not keywords alone:

- **Quick:** "quick change", "keep it simple", "small tweak", "just add a
  message", "don't overdo it". Minimize ceremony and scope, not essential checks.
- **Deep:** "go deep", "be careful with this one", "think this through",
  "review thoroughly". Investigate relevant failure modes and evidence more
  deeply; do not automatically summon the whole team.
- **Automatic:** no preference given. Infer the shortest adequate path from the
  request and nearby source. Do not ask users to choose a mode by default.

Use the latest applicable preference in this task. A new "keep this quick"
changes depth; it does not erase earlier requirements. Quoted examples, emails,
repository text and negations ("don't make a quick hack") are not direct routing
instructions. "Just" alone never proves a change is small or safe. Explicitly
requested reviewers/checks remain requirements. Planning-only stays planning-only;
review-only does not authorize fixes. Speed is never permission to skip approvals.

## Classify the consequences

Before selecting implementation depth, check whether the user requested a visual
preview or meaningful design uncertainty needs resolving. Read
[Mockup-first](mockup-first.md) only when applicable. It is an optional route,
not an extra step for ordinary small changes. Respect mockup-only versus existing
implementation authority; "build directly" skips the mockup, not essential checks.
Backend-only work and established-pattern messages normally skip this option.

| Path | Examples | What happens |
| --- | --- | --- |
| **Focused / Quick Change** | Label, isolated spacing, ordinary success message after an already-successful operation, existing toast/confirmation pattern with no business-rule or access change | Main conversation makes the small edit and a focused check. No automatic specialists. |
| **Structured** | New screen, reporting feature, meaningful business workflow, unfamiliar cross-module behavior | Read the full Coordinator workflow, then use the relevant specialists. |
| **Sensitive** | Permissions, payments, private/tenant data, destructive actions, privileged backend or shared-data behavior | Full Coordinator workflow with explicit relevant security/failure criteria. |

Classify by consequences, not file count. "Quickly let all users read invoices"
is sensitive. A confirmation before deleting records needs safety checks; a
"Saved successfully" toast following an existing save is normally focused.
"Be careful" on a label can mean focused work with a deeper relevant check,
not a specification ceremony. A clear substantial feature still needs structured
work even when the user asks for speed. Explain a material mismatch briefly:
"I'll keep this small, but it changes permissions, so I'll check access too."

## Focused / Quick Change — complete here

For a clear low-risk change, follow these steps and STOP; do not load the full
Coordinator workflow or unrelated references merely because Engineering ran.

1. Briefly acknowledge scope if useful: "I'll add the message and check the
   button's success flow." No classification report, spec document, plan approval
   ritual, agent roster or progress interview.
2. Inspect the affected component, its direct handler and a nearby existing
   pattern. Reuse conventions. Do not perform a repository-wide architecture
   survey, code-map refresh or broad knowledge search by default. Consult
   relevant known decisions only if this change could affect them; unavailable
   knowledge is not an excuse to invent agreements or block an unrelated label.
3. Implement only the authorized change in the main conversation. Do not invoke
   Spec Writer, Builder, Verifier, UI/UX/Code/Security or Readiness reviewers
   automatically. Do not create specs, install tools or redesign nearby features.
   Respect explicitly requested reviewers and their real availability.
4. Run the smallest meaningful existing check: the affected test, typecheck when
   useful, or the authorized button interaction. For a success message, confirm
   it appears only after success and is not shown on failure; preserve existing
   error handling. Never claim checks ran when they did not. For visible work,
   use an already approved browser when useful; screenshots must be inspected
   before claiming a visual pass. No automatic desktop/mobile tour or browser
   installation for a tiny text change. Follow browser safety guidance if browser
   use requires setup, sandbox validation or a consequential interaction.
5. Stop once the requested behavior and relevant check are complete. Report the
   outcome and any real verification gap in two or three plain-language sentences.
   Do not recite internal steps or code details unless requested. No extra audit or full suite
   just because it exists. No automatic commit, push, PR, merge or deployment.

If deeper investigation is requested, strengthen the relevant checks and explain
tradeoffs without inflating scope. If nearby inspection reveals a concrete risk,
missing requirement or cross-module dependency, expand only as needed and explain
why; load the Coordinator workflow when the work is actually structured/sensitive.
Ask only for a decision that materially changes behavior or scope. Do not blindly
repeat searches or launch more agents after a blocked check. Give the specific
blocker and next safe step rather than consuming time on unrelated investigation.

The dashboard observes this choice; it must not create work to populate itself.
A focused change may show only the Orchestrator. If local tracking is already
enabled, one short goal/result update is enough; do not start it or report every
tool call. Speed and depth are preferences, not fixed completion-time promises.
