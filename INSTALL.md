# Abacus Studio for Claude Code

## Install from GitHub

The distribution repository is
[`abacusis/abacus-studio-claude-plugin`](https://github.com/abacusis/abacus-studio-claude-plugin).

Run these commands one at a time using the Claude Code CLI:

```sh
claude plugin marketplace add abacusis/abacus-studio-claude-plugin
claude plugin install abacus-studio@abacus-studio-marketplace
```

Keep the `plugin` part of each command. These are CLI commands, not slash
commands. If you are already chatting with Claude, ask it to run them and review
the installation with you.

Review the plugin and confirm installation for your user account. If Claude asks
to reload plugins, follow that prompt. In Desktop, you can instead open the plugin
manager and add this GitHub repository as a marketplace, then select Abacus Studio.
If your Desktop version has no custom-marketplace entry, use the local Claude Code
terminal commands above or the publisher's ZIP upload option.

You can also ask Claude:

> Help me install Abacus Studio from abacusis/abacus-studio-claude-plugin as a
> plugin marketplace. Review what it installs with me, then help me connect to
> Studio and set up my app. Ask me to complete browser sign-in myself.

A plain chat request does not bypass installation approval or browser sign-in.
A private plugin repository requires GitHub access; a public plugin repository
does not make your Studio apps or client repositories public.

## Connect and start

1. Run `/abacus-studio:connect`. It opens Studio browser approval automatically
   for app access and local development. Complete that one approval yourself;
   never paste passwords, tokens, or Supabase keys into chat. No `/mcp` is required.
2. Choose **Abacus Studio → setup** in the plugin menu, or run
   `/abacus-studio:setup`. Choose your app when prompted.
3. Continue the guided setup and approve the folder and local commands.
   Studio supplies the app's repository, branch and sandbox settings.
4. `/abacus-studio:status` checks your Studio connection and role.
5. Use `/abacus-studio:submit` to review and push changes to the client
   development branch. Use `/abacus-studio:request-publish` to request a
   separate publish PR. Neither command automatically merges or deploys.

Setup reuses the authorization; selecting an app does not require another consent.
Git credentials stay in
your OS credential store. An optional sandbox server key is written to the ignored
local `.env`; local users and coding tools can read it. Production keys are never
appropriate for this workflow.

## Updates and existing ZIP installations

To sign in again, run `/abacus-studio:connect`. It resets the shared helper
authorization and opens a new browser consent flow automatically.
Use `/abacus-studio:disconnect` to revoke that shared authorization without
signing in again. Neither
action deletes your project files. Connect requires fresh Studio approval before
listing apps. Older separately installed connectors remain independent.

Use Claude's plugin manager to refresh this marketplace and update the plugin.
Automatic updates depend on your marketplace settings; they are not guaranteed
merely by publishing a GitHub commit.

For a manual update, refresh the marketplace and then update the plugin:

```sh
claude plugin marketplace update abacus-studio-marketplace
claude plugin update abacus-studio@abacus-studio-marketplace
```

Run `/reload-plugins` after the update, or start a new session.
See [Claude Code's update instructions](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

If you installed Abacus Studio from a ZIP, disable or uninstall that old copy before
enabling the marketplace copy, so duplicate commands and connectors do not appear.
Uninstalling the plugin is not a reason to delete your app workspace.

## Publisher checklist

- Publish only this plugin package to the dedicated distribution repository.
  Do not publish `.env`, `.studio`, `.claude`, credential files, or client app code.
- Validate `.claude-plugin/marketplace.json` and the plugin with `claude plugin validate`.
- Test marketplace installation in a separate Claude profile before sharing it.
- Bump `.claude-plugin/plugin.json` for plugin releases, then publish a matching Git tag.
- A marketplace install does not grant Studio access. Studio still checks each
  user's app membership, enabled local development, and repository authorization.
