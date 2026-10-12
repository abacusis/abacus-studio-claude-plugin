# Disconnect

Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/studio_git.py" disconnect` without
an app ID. It revokes the shared helper consent and clears its saved tokens.
No app selection, folder search, or Claude MCP connector sign-in is required.
The user's Disconnect request authorizes this action. Preserve project files.
Report complete disconnection only after the helper verifies revocation. On a
partial failure, explain that local tokens were cleared but Studio revocation
could not be verified. Never expose token values or edit Claude credential files.

Older separately installed MCP connectors and legacy per-app consents are separate;
this action does not revoke them. Use Studio Connections or the host's sign-out
UI if the user separately requests their revocation. Do not silently broaden
Disconnect to other clients. Sandbox keys already copied locally remain there.

Finish: "Studio is disconnected. Use /abacus-studio:connect to approve access again."
