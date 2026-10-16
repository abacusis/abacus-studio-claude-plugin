# Planning and project language

Read available Studio requirements, relevant conversations and decisions, plus repository conventions. Clearly distinguish retrieved decisions from assumptions. If Studio context is unavailable, continue with available evidence and disclose the gap.

For an ambiguous feature, ask a small number of consequential questions: who uses it, what they need to accomplish, expected success and failure behavior, and which existing workflows must remain intact. Inspect the code for answers before asking the client technical questions it already answers.

Describe the intended behavior and acceptance criteria in the client's language. Identify affected interfaces, data, permissions, and migration requirements. Confirm consequential scope or behavior choices before implementation, without making every routine choice a blocking approval.

Use an existing glossary and architecture decisions if present. Propose additions where ambiguity matters; update them only within the requested work. Do not rewrite historical agreements or create a parallel issue tracker. Studio remains the source for workflow records; Git holds reviewed project documents and source.

For a substantial feature (new workflow, material permissions/data changes, or
several interacting parts), read [Specification-driven planning](specification.md)
and use its spec → plan → tasks → implementation → verification workflow.
Use the same reference when the user explicitly asks for a specification. Small,
well-understood fixes and copy/style changes do not require formal artifacts.
