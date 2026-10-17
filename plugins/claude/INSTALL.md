# Get started with Abacus Studio in Claude Code

Build and preview changes with AI. Save your progress when you want, and ask
Abacus to review it for release when you are ready.

You need Claude Code and access to your application in Studio. Using Codex?
Follow the [Codex instructions](https://github.com/abacusis/abacus-studio-plugin/blob/main/adapters/codex/INSTALL.md) instead.

## 1. Install

Run these commands one at a time in Terminal, or ask Claude to run them for you:

```sh
claude plugin marketplace add abacusis/abacus-studio-plugin
claude plugin install abacus-studio@abacus-studio-marketplace
```

Approve the installation, then restart Claude Code and open a new chat.

## 2. Connect

In Claude Code, enter:

```text
/abacus-studio:connect
```

Sign in to Studio and complete the browser approval when prompted.

## 3. Set up your application

```text
/abacus-studio:setup
```

Choose your application and approve the setup. Claude prepares your local copy
and opens a preview. Your live application stays unchanged.

## 4. Start working

Just describe what you want to change. For example:

> Add a confirmation message after saving.

Try the result and ask for adjustments. You can say “keep it quick,” “go deeper,”
or “show me a mockup first.”

## 5. Save your progress

```text
/abacus-studio:submit
```

Or say: **“Submit my changes.”**

Claude reviews the changes, runs the configured checks, and helps save them to
your shared sandbox repository. This creates a recorded version you can return
to, rather than leaving the work only on your computer. You do not have to be
finished or ready to publish. It does not make the changes live.

## 6. Ask Abacus to publish

```text
/abacus-studio:request-publish
```

Or say: **“Request publishing review.”**

This sends your submitted changes to Abacus for review before release. It does
not automatically publish them. Abacus helps review the work and coordinate the
approved release.

## Get the latest version

```sh
claude plugin marketplace update abacus-studio-marketplace
claude plugin update abacus-studio@abacus-studio-marketplace
```

Then restart Claude Code and open a new chat. If you installed using the previous
`abacusis/abacus-studio-claude-plugin` address, GitHub redirects it to the current
[repository](https://github.com/abacusis/abacus-studio-plugin); try updating normally.

## Need help?

Use `/abacus-studio:status` to check your connection, or contact your Abacus team.
Complete sign-in in the browser; never paste passwords or keys into chat.
