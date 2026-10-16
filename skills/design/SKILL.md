---
name: design
description: Improve your app's design, layout, and accessibility with Impeccable.
argument-hint: "[polish|audit|simplify|critique] [target]"
---

Read and apply [Client communication](../../references/client-communication.md) completely.
Use the project-local Impeccable skill at `.claude/skills/impeccable/SKILL.md`.
For a configured Studio app, first use `abacus-studio:project-knowledge` to retrieve
relevant design/workflow agreements. Only current approved records establish requirements.
Read its complete instructions before taking design actions and follow the
references it selects. Resolve its skill directory to that project-local folder,
not this wrapper's directory, when invoking its launcher or reading references.

Route `simplify` to `distill`; pass other supported actions and the user's target
through. With no action or target, ask which screen or component to improve.
When the user describes a design goal, select the appropriate workflow from
Impeccable's instructions. Do not require subcommands.
Claude can also use Impeccable directly when the user's design request fits.

If the package is missing, explain that Studio setup must install the enabled
design package. Do not fetch an arbitrary latest version or install global skills.
If another Impeccable installation wins name resolution, use the project-local
instructions explicitly so this workflow uses Studio's pinned version.

Do not install hooks or change Claude permissions as part of design work. The
package's engine launcher may download a version-pinned executable on first use;
respect host permissions and report that requirement if blocked. Installation of
skill files is not permission to execute scripts unrestrictedly.

Design work does not authorize submission, publishing, migrations, or production
deployment. Keep credentials and generated local caches out of submissions.
