# Maintaining the public plugin

This is the public Abacus Studio plugin source repository, with separate Claude
and Codex release targets. Shared helpers/playbooks stay here; Codex-only wording
and packaging belong in adapters/codex/ and scripts/build_codex.py. Do not edit
generated distributions or rename the remote as an incidental implementation step.
README.md is the
client-facing product introduction, not an internal architecture manual.

## Every change includes README review

- Update README.md in every change set, including fixes and release changes.
  Explain meaningful user value and newly available capabilities in plain language.
  If there is no user-visible impact, add a brief accurate maintenance note rather
  than inventing a marketing benefit. Do not make empty/whitespace-only edits.
- Look for an honest opportunity to promote improvements: why they help clients,
  how they improve on unguided AI coding, and what users can now do more easily.
- Keep the latest version heading, release availability, specialist roster, commands,
  setup and update guidance synchronized with actual implementation. During release
  preparation say unpublished; only change that wording when publication is authorized.
- Preserve access, evidence, review, and publishing boundaries. Never market source
  review as a penetration test, evidence review as independently executed testing,
  or AI readiness as human approval. Do not promise unimplemented capabilities.
- Keep README concise and marketing-facing. Put implementation detail and full
  evidence in RELEASE.md and references/ rather than adding an endless changelog.
- Before handoff run `python3 scripts/check_readme.py`, package tests, and relevant
  regression tests. For a multi-commit change use `--base <starting commit>` to check
  README changed somewhere in the change set. CI enforces this for pushes and PRs.
- Include README.md, synchronized manifests and release notes in an approved release
  commit. Implementation approval does not authorize commit, push, tag, or publication.

The automated check catches missing updates, mismatched version headings, and a
missing specialist introduction. Human review still checks honesty and usefulness;
changing a file is not proof that the copy is good.

For cross-host changes, test both release targets. Preserve existing Claude
entrypoints. Codex instructions must not assume Claude agent registration or
environment variables. Dashboard attribution and delegation limits must stay
explicit. No installation, hook-trust bypass or remote publication as a build step.
