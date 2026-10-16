# Publishing Abacus Studio for Claude Code

Target repository: `abacusis/abacus-studio-claude-plugin`.
Internal plugin: `abacus-studio`; marketplace: `abacus-studio-marketplace`.
Only the plugin distribution belongs in this repository.

## Prepare a release

1. Bump both plugin/marketplace manifests and the version assertion. Update
   README.md in every change set: highlight meaningful new client value, keep its
   latest-feature heading and specialist roster current, and distinguish locally
   prepared features from published releases. Add the release notes here. See
   AGENTS.md for the ongoing documentation rule. Do not invent benefits for
   internal-only changes; use a short maintenance note instead.
   Run `python3 scripts/check_readme.py --base <starting commit SHA>` to check the
   whole change set. CI requires a README change for every push/PR with changes.
   The release builder also checks README version and specialist coverage.
2. Run the Python tests and `node --test tests/package.test.mjs`.
3. Run `claude plugin validate .`.
4. Use `scripts/build_release.py --output <NEW absolute release folder>`.
   It copies only allowlisted distribution files, rejects symlinks and concrete
   credential patterns, and writes file hashes and a verified ZIP beside the
   clean folder. It never initializes Git, pushes, or changes repository visibility.
5. Review the audit manifest. Do not upload the development folder wholesale:
   local `.claude` settings, caches, `.env`, and application workspaces are excluded.

## Before publishing

- Review README marketing claims against actual implementation and evidence.
  Once publication is authorized, replace the current local/unpublished notice
  with accurate release availability before including README in the release commit.
  Do not promise working interactions from screenshots or certified security.

- LICENSE currently contains a proprietary review draft, not adopted terms.
  Do not publish it as effective until legal review and owner approval confirm
  the licensor, ownership, acceptance process, client agreement consistency and
  governing terms. Preserve THIRD_PARTY_NOTICES.md and all upstream MIT notices.
  Public visibility alone does not grant an open-source license.
- Create a NEW dedicated repository from the clean folder, not another project's
  history. Check the initial commit for secrets before making it public.
- Test marketplace installation in a separate Claude profile and a clean app
  workspace, including Studio sign-in, setup, and a manual plugin update.
- Test Windows and Linux separately; current automated tests are not those tests.
- Publish a matching version tag after approval. Protect the distribution branch
  and review updates: clients enabling auto-update trust code released here.

## 0.24.0

- Adds a read-only Readiness Reviewer to reconcile current requirements, checks
  and relevant specialist findings before declaring substantial work ready.
- Missing/stale evidence and material unresolved validation cannot become passes;
  actual defects take priority while evidence gaps stay visible.
- Preserves the shared two-round correction limit and separate publishing approval.
- Updates the public README with the client benefit and current specialist team.

## 0.23.0

- Adds a read-only UX Reviewer to assess actual flow evidence, feedback and recovery.
- Keeps UI presentation review distinct from task completion and executed checks.
- Refreshes the public README to explain the specialist team and its client value.
- Adds a standing README maintenance rule, CI change-set check, and release-time
  version/specialist coverage checks. These are structural checks, not editorial QA.
- No automatic publication, extra credentials, or new runtime access.

## 0.15.0

- Adds read-only application knowledge search/retrieval through the helper.
- Engineering and Design retrieve relevant records before consequential changes.
- Preserves explicit sharing, approval/lifecycle distinctions and app permissions.
- Requires Studio's application knowledge migration and matching MCP deployment.

## 0.14.1

- Publishes a clearly labeled proprietary license draft naming Abacus Internet
  Solutions Inc.; it is not effective terms and does not alter prior releases.
- Includes third-party notices and full upstream MIT attribution in packaging.
- No runtime, permission, or command changes.

## 0.14.0

- Adds specification-driven planning to Engineering for substantial features.
- Links requirements, implementation tasks, and actual acceptance evidence.
- Includes Spec Kit attribution and MIT notice; no extra installer or commands.
- Preserves existing standards, branch handling, migration and release approvals.

## 0.13.0

- Adds Abacus Security for focused source-only reviews and optional direct use.
- Routes materially security-sensitive Engineering changes to the security skill.
- Includes Cloudflare attribution and MIT notice; preserves Studio approvals.
- No full audit harness, target execution, live probes, or dashboard upload.

## 0.12.0

- Adds Abacus Engineering: one automatically discoverable skill and an optional
  `/abacus-studio:engineering` command for planning, testing, debugging,
  architecture, and review.
- Bundles curated Abacus playbooks with upstream attribution and the MIT notice.
- Preserves Studio's submission, sandbox approval, and publishing boundaries;
  adds no credentials, hooks, or automatic commits or deployments.
- Verifies the engineering references are included in release archives.

## 0.11.3

- Refreshes the client-facing plugin description in both manifests.
- Keeps marketplace version and description synchronized with the plugin manifest.
- No permissions, commands, authentication, or application behavior changes.

## 0.11.2

- Public-release packaging uses an explicit allowlist and hashes every included file.
- Excludes local permissions, credential files, Python caches, and Git history.
- Installation and update instructions use the dedicated Claude plugin repository.
- Removes client-name references from a package test fixture.
- Adds Supabase management-token detection to the submission secret guard.
- Documents credential boundaries, execution risks, and platform test limitations.
