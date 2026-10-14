# Publishing Abacus Studio for Claude Code

Target repository: `abacusis/abacus-studio-claude-plugin`.
Internal plugin: `abacus-studio`; marketplace: `abacus-studio-marketplace`.
Only the plugin distribution belongs in this repository.

## Prepare a release

1. Bump `.claude-plugin/plugin.json` and the release notes/version assertion.
2. Run the Python tests and `node --test tests/package.test.mjs`.
3. Run `claude plugin validate .`.
4. Use `scripts/build_release.py --output <NEW absolute release folder>`.
   It copies only allowlisted distribution files, rejects symlinks and concrete
   credential patterns, and writes file hashes and a verified ZIP beside the
   clean folder. It never initializes Git, pushes, or changes repository visibility.
5. Review the audit manifest. Do not upload the development folder wholesale:
   local `.claude` settings, caches, `.env`, and application workspaces are excluded.

## Before publishing

- Choose an explicit license/usage policy. Public visibility alone does not grant
  an open-source license; no license has been selected in this package.
- Create a NEW dedicated repository from the clean folder, not another project's
  history. Check the initial commit for secrets before making it public.
- Test marketplace installation in a separate Claude profile and a clean app
  workspace, including Studio sign-in, setup, and a manual plugin update.
- Test Windows and Linux separately; current automated tests are not those tests.
- Publish a matching version tag after approval. Protect the distribution branch
  and review updates: clients enabling auto-update trust code released here.

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
