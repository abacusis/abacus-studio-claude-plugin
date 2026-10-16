---
name: request-publish
description: Request review through a client-repository sandbox-to-main PR, without merging or deploying.
disable-model-invocation: true
---

# Request publish

This is distinct from Submit: Submit saves commits on the client development
branch. Request publish opens a PR to Studio's configured client release branch.
Never push directly to the release branch, merge the PR, or invoke deployment.

1. Use the setup interpreter and selected authorized Git workspace. Run
   `studio_git.py publish-preview --project-id "<Studio ID>" --workspace "<absolute workspace>"`.
   It fetches first and refuses dirty or unsynchronized workspaces. If needed,
   finish Submit separately with its own confirmations before continuing.
2. The backend verifies membership, separate private repository and distinct
   development/release branches. Opening the review PR does not require branch
   protection or a paid GitHub plan. Existing GitHub rules remain unchanged and
   apply to any later merge. The server needs Pull requests Write permission to
   create PRs; it does not request Administration Read for protection inspection.
   These are never client tokens. Report actual server errors; do not invent a
   branch-protection prerequisite or change repository rules or billing.
3. If no changes exist, say so. If an open PR exists, show its link; do not duplicate
   it. Otherwise review the returned commit messages and file list, draft a factual
   title and description, and ask the client to confirm the publish request.
   Describe this as a request for review, not a successful publication.
4. Run `studio_git.py publish --project-id "<Studio ID>" --workspace "<absolute workspace>" --approved`
   with JSON on stdin containing ONLY title, description, expected_head and
   expected_base. Use exact SHAs from preview. Do not print secrets or call the
   credential helper. If branches moved, refresh preview and obtain approval again.
5. Show the returned PR link and state that it awaits review. No merge/deploy occurs.
   Later sandbox pushes update the PR; reviewers must check its latest diff.
