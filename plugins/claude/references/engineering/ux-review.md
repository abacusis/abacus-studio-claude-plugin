# Review how the task works

UI review checks presentation. UX review checks whether people understand and can
complete the intended task. Functional assertions and UX judgments complement
each other; passing a selector assertion does not prove a sensible experience.
This is a bounded change review, not a scored whole-app audit or redesign.

## Handoff and evidence

Give the reviewer the authorized flow, intended user/role, goal, accepted criteria,
source/version including local edits, and relevant existing decisions. The
coordinator or authorized verifier supplies actual approved browser actions and
assertions with results, route/state/viewport, capture time, screenshots and origin.
Identify synthetic fixtures, manual observations, and supplied evidence honestly.
Do not include real customer data or credentials. Missing optional design packages
do not block basic UX review; relevant approved guidance can be supplied as context.

The UX Reviewer has only Read/Grep/Glob; it cannot operate a browser or run scripts.
The coordinator owns the approved browser facility, sandbox confirmation, sign-in
handoff, and any additional write authorization. Never repeat real submissions or
destructive actions just to get evidence. A test plan is not an executed check.
Read screenshots as images before visual claims, but do not mistake static images
for evidence that navigation, validation, saves, or recovery actually worked.

## Check the relevant experience

- Clear labels, next steps and navigation for the accepted user and task.
- Relevant feedback: loading, completion, validation failures and permissions.
- Empty/error states that explain what happened and offer a useful next action.
- Recovery: preserved input, retry/cancel/back behavior, no misleading success.
- Relevant keyboard/focus and accessible feedback, only to the extent observed
  through actual keyboard actions, accessibility evidence or source inspection.
- Mobile/task context where supplied; avoid inventing personas or requirements.

Test only states relevant to the change and distinguish not applicable from not
tested. A stale, missing, inaccessible or failed capture cannot support a pass.
Changed source or flow state invalidates affected evidence; request refreshed
checks rather than silently reusing a previous review. New required behavior must
be proposed to the coordinator, not retroactively added to the accepted spec.

## Findings and limits

Tie observed failures to criterion, step/state, source identity, actual action and
result, evidence path and reporter. Explain user impact and a narrow remedy, with
an affected recheck. Keep source-grounded risks and optional improvements separate.
Source inspection can explain a defect, not establish that a browser test ran.
Missing interaction evidence means not flow-verified; missing mobile or role checks
leave those areas not verified. Do not infer backend persistence from a success
message or claim accessibility compliance without the required checks.

Return findings to the coordinator; fixes require authorization and fresh affected
flow evidence within the existing two-round correction limit. Relevant material
UX gaps prevent a readiness claim. Neither UX review nor a working preview grants
Abacus approval, permission to commit/push, or authorization to publish.
