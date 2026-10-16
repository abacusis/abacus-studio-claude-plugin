# Maintainable boundaries

Inspect existing architecture and decisions before proposing changes. Prefer a small stable public interface hiding meaningful implementation complexity. Keep behavior near the data and responsibilities it belongs to; separate business policy from external adapters when this improves testability or change locality.

Evaluate proposals against the actual feature: which callers change, how behavior is tested, migration and compatibility costs, and how failures propagate. Reuse established patterns unless evidence justifies a departure.

Treat naming problems, duplicated policy, repeated switches, and scattered edits as signals to investigate, not automatic violations. Do not create an abstraction for hypothetical future needs. Do not refactor unrelated modules while fixing a localized bug.

For an architecture survey, present candidates and tradeoffs before implementing a broad refactor. Preserve public behavior and add appropriate checks when changing boundaries. Record a consequential accepted decision in the project's existing decision system, with rationale and alternatives, rather than silently changing conventions.
