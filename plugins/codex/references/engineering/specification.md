# Specification-driven planning

Use for substantial features or explicit specification requests. This is a
lightweight adaptation, not a Spec Kit installation. Do not run `specify init`,
install Python/uv, generate `.specify` tooling, execute extension hooks, or change
Git branches. Studio's existing standards and authorization remain authoritative.

## 1. Establish the agreement

Read available project decisions, the requested feature, and existing behavior.
Reuse an existing relevant spec rather than starting competing documents. Resolve
consequential unknowns with a few plain-language questions. Do not invent privacy,
retention, permission, or performance requirements as industry-standard defaults.
Separate assumptions from retrieved decisions and confirmed requirements.

Draft the business specification using the outline below. Describe what users
need and why, not framework choices. Use stable requirement IDs for later
traceability. Include relevant failure/permission cases and explicit non-goals.
Do not invent numeric targets: outcomes may be verifiable behavior rather than
unsupported performance promises.

For a clear, authorized implementation request, summarize the requirements and
proceed; do not add a mandatory approval pause. Ask for confirmation when an
unanswered question materially changes behavior, scope, or a current agreement.
Previously confirmed requirements need not be approved repeatedly.
Planning-only requests stop at the requested artifact;
approval of a plan alone is not permission to build, migrate, submit, or publish.

## 2. Decide how it fits

Prepare a technical plan grounded in the existing application and Studio settings.
Identify affected modules, interfaces, data, permissions, compatibility, testing,
and any migration needs. Record important choices, reasons and alternatives.
Flag unresolved blockers instead of describing guesses as completed research.
Do not replace project standards with a new constitution or assume a greenfield
stack. Route security-sensitive work to Abacus Security and interface design to
the existing Design capability where relevant.

## 3. Make executable tasks

Break implementation into small end-to-end slices. Give each task its affected
requirement IDs, dependencies, expected behavior, and verification approach.
Do not turn every file edit into a ticket or manufacture a parallel issue tracker.
Propose parallel work only when the host supports it and boundaries are independent.

## 4. Implement and verify

When implementation is authorized, use Engineering's testing, architecture and
review playbooks. Keep task status current: planned, in progress, implemented,
verified, or blocked. Implemented is not verified. Record the actual checks and
their results; a source review or self-completed checklist is not a passing test.

At completion, compare every requirement to the code and evidence. Report met,
partial, not met, or not verified. Identify regressions and scope additions.
If code reveals a needed requirement change, propose it for confirmation rather
than rewriting the agreement to make the implementation look correct. Preserve
the rationale and prior decisions when updating an accepted spec.

Fix identified gaps only within authorized scope, then recheck relevant outcomes.
Stop and report missing access, failed checks, or unresolved decisions; do not run
an unbounded convergence loop or claim completion with hidden gaps.

Saving remains `$abacus-submit`; publishing review remains
`$abacus-request-publish`. A checked-off spec does not bypass either.

## Artifact placement and outline

Keep small plans in chat when sufficient. For a substantial feature, use the
project's existing documentation/spec location. If none exists, propose
`docs/specs/<feature-slug>.md` and confirm placement before creating it. Keep one
document unless complexity warrants separate files. Do not overwrite an existing
spec; inspect and update it in place or select a distinct name. Project documents
are normal reviewed Git changes, not ignored plugin metadata or secrets. Do not
claim they were uploaded to Studio: dashboard linkage is not implemented.

Use this outline, replacing prompts with actual content and omitting irrelevant
sections. Do not leave scaffold placeholders or speculative requirements.

1. **Feature and status** — business purpose, source request, draft/accepted state.
2. **Scope** — included behavior and non-goals.
3. **Requirements** — R1, R2…; actor, behavior, and acceptance scenarios, including
   relevant errors and access constraints.
4. **Decisions and open questions** — confirmed choices, assumptions, blockers.
5. **Technical plan** — affected interfaces/data, compatibility, alternatives,
   approved validation commands and migration review needs.
6. **Tasks** — T1, T2…; linked requirements, dependencies, status, verification.
7. **Acceptance evidence** — requirement ID, outcome, test/manual check, actual
   result, and remaining limitation. Clearly distinguish planned checks from runs.

See [Spec Kit provenance and license](spec-kit-upstream.md).
