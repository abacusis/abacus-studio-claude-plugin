# Application knowledge deployment and use

Version 0.15.0 requires Studio's app knowledge migration plus updated
`project-planning`, `mcp`, and any functions importing `project-context.ts`.
Deploy backend/schema before distributing this plugin version, then deploy the
Studio UI. No OAuth scope change is needed: the two read-only tools use
`projects:read` and recheck active app membership.

Abacus administrators open the application's Knowledge tool (also linked from
Context when an app is selected), create a curated record, and explicitly enable
AI/plugin sharing. Saving returns a record to Proposed; shared approval and
lifecycle actions require an Abacus administrator. Existing records remain
unshared until explicitly selected. Do not publish confidential internal context
or credentials. Unshared records are also excluded from Studio's existing AI
context loader; its approved excerpts stay bounded in size.

Discovery returns titles, summaries, optional topics, source metadata and status.
The hidden project-knowledge skill reads full relevant records and distinguishes
current approved requirements from proposed/superseded context. Archiving removes
records from plugin discovery and retrieval. The existing planning history retains
changes; there is no automatic ingestion or plugin knowledge-write tool.

Verify with one shared approved decision, a shared proposal, a superseded decision,
and an unshared record. A member should discover only shared records from their
selected app; another app's record ID and revoked membership must not grant access.
Ask for a change contradicting the approved decision: Claude should explain the
rationale and request confirmation, not permanently veto or silently edit it.
Backend failure must be reported as unavailable knowledge, not an empty library.
