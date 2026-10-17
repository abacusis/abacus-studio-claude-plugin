# Get started with Abacus Studio in Codex

Build and preview changes with AI. Save your progress when you want, and ask
Abacus to review it for release when you are ready.

You need Codex and access to your application in Studio. Use the same guided
workflow as Claude Code, adapted to Codex's skills and project specialists.

## 1. Install

Run these commands one at a time in Terminal, or ask Codex to run them for you:

```sh
codex plugin marketplace add https://github.com/abacusis/abacus-studio-plugin.git
codex plugin add abacus-studio@abacus-studio-codex
```

Approve any installation prompts, then restart Codex and open a new chat.

## 2. Connect

In Codex, enter:

```text
$abacus-connect
```

Sign in to Studio and complete the browser approval when prompted.

## 3. Set up your application

```text
$abacus-setup
```

Choose your application and approve the setup. Codex prepares your local copy
and opens a preview. Your live application stays unchanged.

Version 0.29.0 includes eight project-scoped AI specialists in approved
setup. After their first setup, open a new chat in the project so Codex can load
them. Existing projects can ask: “Refresh this project's Abacus specialists.”
No global Codex settings are changed.

## 4. Start working

Just describe what you want to change. For example:

> Add a confirmation message after saving.

Try the result and ask for adjustments. You can say “keep it quick,” “go deeper,”
or “show me a mockup first.”

## 5. Save your progress

```text
$abacus-submit
```

Or say: **“Submit my changes.”**

Codex reviews the changes, runs the configured checks, and helps save them to
your shared sandbox repository. This creates a recorded version you can return
to, rather than leaving the work only on your computer. You do not have to be
finished or ready to publish. It does not make the changes live.

## 6. Ask Abacus to publish

```text
$abacus-request-publish
```

Or say: **“Request publishing review.”**

This sends your submitted changes to Abacus for review before release. It does
not automatically publish them. Abacus helps review the work and coordinate the
approved release.

## Get the latest version

```sh
codex plugin marketplace upgrade abacus-studio-codex
codex plugin add abacus-studio@abacus-studio-codex
```

Then restart Codex and open a new chat.

## Need help?

Use `$abacus-status` to check your connection, or contact your Abacus team.
Complete sign-in in the browser; never paste passwords or keys into chat.
