# Review the visible result

UI review checks presentation; UX review checks whether people can complete tasks.
Keep them distinct. This playbook is for a bounded review, not a new design system,
a scored whole-app audit, or the full optional Impeccable critique workflow.

## Establish visual evidence

The coordinator identifies the changed source and correct approved preview, then
uses the existing browser-verification workflow to capture relevant desktop and
mobile states. Handoff image paths, viewport sizes, route/state, capture time,
source identity (including local edits), relevant design agreements, and optional
before/reference captures with their provenance. Never label a fixture or mockup
as evidence of the real application. Missing metadata limits review confidence.

Open images using an image-capable tool. Capture success is not visual inspection.
If no readable images exist, request them and report not visually verified. Source
review alone may identify a risk but cannot establish a rendered defect or pass.
Do not reuse stale images after relevant edits; request new captures and invalidate
affected findings. A matching Git HEAD alone does not prove a local render is fresh.

## Inspect proportionately

- Clipping, overlaps, obscured actions, overflow, and text wrapping/truncation.
- Alignment, spacing, density, and grouping relative to the existing design.
- Typography, visual hierarchy, readable labels, icons, and action emphasis.
- Consistency of components, colors and states across supplied captures.
- Desktop/mobile composition, long-content handling, and visible empty/error states
  when supplied. Do not invent states that were not captured.

Preserve product facts, accepted constraints and the incumbent visual identity.
Optional Studio-managed Impeccable guidance can inform review when supplied; do
not run its scripts or full audit from this read-only agent. The coordinator uses
Design only for separately authorized design work. Do not install anything because
optional guidance is unavailable. Distinguish demonstrable presentation defects
from taste-based suggestions. Intentional scroll regions are not automatically bugs.

## Report what the images support

Prioritize observed user impact: blocking obscured content/action, major readability
or layout problem, minor inconsistency, optional polish. Describe image and region,
not invented numerical bounds. Exact contrast/size/accessibility claims require
actual measurement; screenshots alone do not establish keyboard operation, ARIA,
screen-reader support, complete flow success, or accessibility certification.

Include inspected images, source provenance, findings, narrow proposed remedies,
optional suggestions, and gaps. Missing mobile images leave mobile not verified;
missing reference images leave comparison unavailable. No visual issues in a
snapshot is not proof of a working feature, UX approval, or readiness to publish.
The coordinator consolidates findings, routes authorized fixes to Builder, and
requests fresh evidence within the existing two-round correction limit.
