# Focused source review

## Establish scope

Identify the feature, files, or diff under review and its intended behavior. Record the current commit and whether the working tree is dirty. Include staged, unstaged, and relevant untracked source when reviewing current changes; committed HEAD alone misses work. Use read-only local inspection, not a fetch or another Git mutation. If no baseline is available, disclose it.

Read the entry points, callers, authorization controls, data access and output handling needed to follow the in-scope paths. Inspect relevant schema or policy source when available; do not infer the deployed Supabase RLS settings from frontend code. Do not read `.env` or credential stores to assess configuration: use variable names, examples, and references in source. Redact any accidentally encountered secrets and personal data; cite their locations without reproducing values.

## Follow trust boundaries

For each candidate identify: the lower-trust actor, accepted input or action, intended control, reachable code path, affected resource or other principal, and the concrete security outcome. Check applicable paths, not every category regardless of scope:

- Authentication and authorization: server-side checks, ownership and role enforcement, admin handlers, session handling, and cross-user access.
- Tenant/data isolation: caller-controlled IDs, queries, exports, caches, and source-defined RLS policies. Distinguish service-key authority from a reachable unauthorized caller path.
- Injection and output handling: SQL construction, shell calls, template/HTML rendering, URL or file-path handling, and upload constraints.
- Secrets and integrations: client-bundled privileged variables, error/log disclosure, webhook signature handling, and server-to-server trust.
- AI/tool features: untrusted prompts or retrieved content influencing privileged tool arguments, authorization, or unsafe output use.

Trace the actual path and consider defenses elsewhere. Missing defense-in-depth, a dangerous-looking function with no reachable input, or intended access to one's own data is not automatically a vulnerability. Provider settings, gateway behavior and identity configuration absent from source are unknown, not presumed missing.

## Verify without running an attack

Try to disprove each candidate by inspecting guards, callers and relevant source. Existing test source can inform the analysis but is not evidence a test was run or passed.

Where authorized independent delegation is available, give a fresh reviewer the candidate and the minimum source evidence needed to check it. Do not give them credentials or allow target execution, source edits, network probes, or production access. Request a concrete counterexample or verified trace. Deduplicate candidates by root cause and affected boundary.

Use these result labels:

- **Needs validation:** a plausible source-grounded boundary failure with an exact unresolved fact. No severity. Identify whether independent verification, safe execution, or deployment configuration is missing and who can establish it.
- **Rejected:** the candidate was disproved; briefly state the relevant control or incorrect assumption.
- **Confirmed:** only if independent evidence establishes the complete boundary failure and actual result. Source suspicion or a second agent agreeing is not an observed runtime result. This source-only version will commonly produce needs-validation candidates rather than confirmations.

Keep ordinary hardening recommendations separate from vulnerabilities. Do not manufacture a health score or count unresolved candidates as confirmed problems.

## Report

Return a concise chat summary by default. For each actionable candidate give a stable local identifier, title, file/line evidence, actor and affected resource, trace, established facts, unresolved fact, and narrow proposed fix with a regression-test idea. Severity applies only to confirmed findings and must reflect demonstrated impact, not hypothetical worst cases.

State reviewed paths/revision, source-only methodology, independence status, and limitations. Do not turn a partial review into a whole-app safety claim. Do not write artifacts unless requested. If a report is requested, use an explicitly approved location outside source or verified Git-ignored directory, excluding secrets and customer data. This version does not emit upstream-schema-validated JSON or upload findings to Studio.
