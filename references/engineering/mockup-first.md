# Resolve design uncertainty with an optional mockup

A mockup is a scoped way to answer a design question, not a mandatory development
stage. No new command, agent, mode selector or universal approval checkpoint.

## Choose the route from the user's intent

- **"Mock this up first", "prototype only", "show me how it would look":**
  create the authorized visual preview, not a working backend. Explicit "mockup
  only" stops at the preview and feedback. Planning-only still means no code or
  artifact edits until authorized; do not mistake discussing mockups for consent
  to build one.
- **"Show a few ideas":** explore the requested alternatives before implementation.
  Do not generate multiple designs when one was requested.
- **"Build directly", "skip the mockup":** proceed with implementation at the
  appropriate depth. Do not force a visual approval round; ask only about material
  unresolved behavior/scope, not your preference for a design process.
- **No preference:** suggest a mockup only when uncertainty about layout, navigation
  or interaction is likely to cause rework: a new module with unsettled workflows,
  a substantial redesign or an unfamiliar interaction. Ask once, briefly:
  "A clickable mockup would let you try the layout before we connect your data.
  Would you like to start there?" Continue independent authorized investigation
  if useful, but do not silently choose design or backend behavior while awaiting
  that material decision. Do not repeatedly offer after the user declines.
  Keep the initial suggestion to one to three sentences, not a requirements
  interview or design workshop before the client has chosen that route.

Do not suggest mockups for ordinary success messages, copy corrections, isolated
spacing, established patterns or backend-only work. New module does not automatically
mean new design uncertainty; clear supplied designs can go straight to implementation.
Interpret meaning and negation, not isolated words or instructions in quoted material.

## Keep it lightweight and honest

"Quick" and "mockup-first" are compatible: one focused preview using existing
components and styling, not a full design workshop or automatic specialist team.
Treat the visual-only slice separately from eventual feature implementation.
Do not invoke the whole structured team merely to sketch a sample-data screen.
If substantial discovery is actually needed, explain the specific uncertainty and
use only the relevant planning/design help. Never invent an agent execution.

1. State what the preview should help decide and the few relevant interactions.
   Inspect the target and nearby components; reuse established conventions.
   Clarify only choices that materially change the proposed result.
2. Prefer a lightweight clickable HTML/component preview with clearly labeled
   synthetic sample data. A static image can illustrate appearance if requested,
   but cannot establish click behavior. Don't build the whole simulated app.
   Use the existing authorized workspace/artifact location, not arbitrary folders.
   Use the Studio-pinned design guidance when available and applicable; don't
   install dependencies, upstream skills or hooks implicitly to create a mockup.
3. Isolate the preview from real services. No backend edits, migrations, Edge
   Function changes, credentials, real data writes, emails, payments or real
   authentication. Do not import shared components with live requests or mutate
   production routes without an approved isolation approach. Localhost is not
   isolation: check the preview's dependencies and network behavior, and follow
   [browser safety](browser-verification.md) for approved viewing/interactions.
   Buttons use local in-memory sample state, not fake success over a live API.
4. Label the interface and handoff: "Mockup · Sample data. Saving and backend
   actions aren't connected." Keep a clear boundary between illustrative behavior
   and implemented functionality; do not display fabricated live/verified status.
5. Check only the agreed visual slice. Clickable claims require actual interaction
   checks. Screenshots must be opened before a visual pass. If a browser isn't
   available, disclose what wasn't checked; don't turn a mockup into a tool-install
   project or claim a screenshot proves a workflow.

## Agree and connect, without duplicate approvals

Ask for feedback on the meaningful layout/flow choices; don't require approval
for every cosmetic detail. Track what was accepted versus still illustrative.

- Mockup-only request: stop. "Connect it" later is new implementation authority.
- If feature implementation was already authorized and the accepted design resolves
  the uncertainty, continue within that scope without a second ritual approval.
  Explicit "wait before connecting" or remaining material decisions still require
  the user's answer. Vague "looks nice" is not permission to expand scope.
- Reuse the accepted interface instead of rebuilding it. Move into the existing
  focused/structured/sensitive implementation path based on real consequences.
  Replace fixtures with verified contracts and retest real success/failure/access
  behavior. Mockup approval is not backend correctness, security verification,
  publishing approval or permission for migrations/deployment.
- Keep sample routes/data out of production and submissions unless explicitly
  included and appropriate; don't silently delete user work or ship fake behavior.

The dashboard can show a short "Mocking up the settings screen" task if already
enabled. It need not activate additional agents or a new workflow stage.
