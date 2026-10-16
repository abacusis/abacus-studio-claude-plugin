# Review the actual change

Establish the intended scope and comparison baseline. Inspect committed outgoing changes, staged changes, unstaged changes, and relevant untracked source; `HEAD` alone can miss the client's work. Use an explicit baseline or the workspace's verified tracking branch, and disclose any unavailable comparison. Do not fetch or mutate Git here as a shortcut around Submit's helper.

Review two distinct questions:

1. **Requirements:** does the change implement the agreed behavior and acceptance criteria, including failures and permissions? Is anything missing or outside scope? If no spec exists, use the user's request and label uncertainty.
2. **Engineering:** does it follow project standards, preserve compatibility, handle errors, protect secrets and access boundaries, and include meaningful verification? Distinguish demonstrable defects from maintainability suggestions. Avoid repeating issues already enforced by passing tools.

Use file and line evidence, impact, and a proposed remedy for actionable findings. Prioritize correctness, authorization, data exposure, and regressions over stylistic preferences. Do not claim exhaustive security coverage.

When a feature specification exists, check each requirement ID against behavior
and actual acceptance evidence, including task dependencies and verification gaps.
Do not rewrite the spec to fit the code or count implemented tasks as verified.
Report met, partial, not met, and not verified separately. Use the accepted version
and identify proposed requirement changes rather than silently treating them as agreed.

Report both axes separately, plus executed checks and remaining uncertainty. If authorized and supported, independent reviewers can review each axis; otherwise perform both explicitly without pretending subagents ran. Do not automatically fix findings in a review-only request.

Development review does not approve a commit, push, release, or production deployment. Submission and publishing remain separate Studio workflows.
