# Abacus Studio for Claude Code

## Build your software with AI, without doing it alone.

“I wish our software could do this.”

Abacus Studio helps you turn that idea into a change you can see and test—using
Claude Code, connected to your application and backed by Abacus's engineering
guidance and review process.

Keep using the AI tool you know. Describe what you want, preview the results,
and work with Abacus to bring reviewed changes into your live application.

[Get started](https://studio.abacusis.ca/install/claude) ·
[Explore Abacus Studio](https://studio.abacusis.ca)

## More than a connection to your code

Claude Code provides the AI. The Abacus Studio plugin adds project context,
engineering playbooks, and a guided path from local development to review.

**Knowledge of your application.** Claude can retrieve relevant decisions,
agreements, and prior reasoning explicitly shared through Studio. You don't have
to explain the same background every time. Previous decisions inform the
conversation; they don't permanently prevent changes.

**Engineering guidance built in.** Abacus Engineering provides playbooks for
clarifying requirements, planning features, testing, debugging, and reviewing
code. Larger changes get a structured approach; small improvements stay simple.
For substantial features, a read-only Spec Writer agent can help clarify the
requirements before implementation, while Claude coordinates the work.
An implementation Builder agent can then work from those requirements, with
a Verification Specialist checking the result against agreed requirements.
It reports what passed, what failed, and what still needs checking. A read-only
Code Reviewer examines the engineering quality and potential regressions.
Abacus technical review and publishing approval remain separate.

**Design and security support.** Improve layouts and usability with the optional
Studio-managed Impeccable design package. Focused source reviews help identify
potential security issues and explain what still needs verification. They are
not a substitute for a complete security audit.
For sensitive changes, a read-only Security Reviewer traces relevant access and
data boundaries and reports concerns without probing your live application.
A UI Reviewer inspects actual desktop/mobile screenshots for layout problems
and visual consistency, keeping visual review separate from workflow testing.

**A clearer view of the code.** When enabled for your application, a local code
map helps Claude locate related components before making substantial changes.

**Plain-language communication.** The plugin guides Claude to explain results
and next steps simply, with technical detail when you need it.

**See the result, not just the code.** Approved local browser checks can exercise
the changed flow and capture desktop and mobile-sized screenshots for inspection.
The plugin can reuse available browser tools or offer a managed Playwright setup.
Screenshots alone do not prove the feature works or replace your review.

These capabilities guide Claude's work; they don't guarantee correct code or
replace testing and professional review. Availability depends on your app's
Studio configuration.

## From your idea to your live application

1. **Set up your app.** Sign in to Studio, choose your application, and let guided
   setup prepare its code and local preview with your approval.
2. **Describe your change.** Ask Claude what you want to improve. Work through
   the plan, try the result, and refine it together.
3. **Save your progress.** Submit reviewed changes to your sandbox repository,
   so they aren't stored only on your computer. You don't have to be ready to
   publish.
4. **Request publishing review.** When you're ready, send the changes for review.
   Abacus can review them with you and coordinate the publishing process.

**Saving is not publishing.** Submitting saves changes to the sandbox repository.
Requesting publish opens a separate review request. Neither command automatically
merges changes or deploys your application.

## Get started

You'll need Claude Code and access to an application configured for local
development in Abacus Studio. The public plugin does not grant access to any
client's application, code, or data.

Follow the [installation guide](https://studio.abacusis.ca/install/claude), then
run this in Claude Code:

```text
/abacus-studio:setup
```

Setup guides you through sign-in, app selection, and approval of the local setup.
After that, just describe what you'd like to change.

> “Help me add a sales dashboard showing monthly revenue and recent orders.”

## Useful commands

You can describe your development goals naturally. These commands are shortcuts
for specific Studio actions:

| Command | When to use it |
| --- | --- |
| `/abacus-studio:setup` | Prepare your app and open a local preview. |
| `/abacus-studio:connect` | Sign in or renew your Studio connection. |
| `/abacus-studio:status` | Check your connection, role, and access. |
| `/abacus-studio:engineering` | Get help planning, building, debugging, or reviewing. |
| `/abacus-studio:design` | Improve a screen's design or usability. |
| `/abacus-studio:security` | Request a focused source-code security review. |
| `/abacus-studio:submit` | Review and save changes to the sandbox repository. |
| `/abacus-studio:request-publish` | Send your changes for publishing review. |
| `/abacus-studio:disconnect` | Revoke the plugin's Studio connection. |

## Your project stays yours

Studio checks your access to the assigned private client repository. Sign-in
credentials use your computer's secure credential store. If your app needs
sandbox keys, authorized setup can place them in a local, Git-ignored environment
file; local users and coding tools can read that copy. Never use production keys
for this workflow or paste credentials into chat.

See [security and access details](SECURITY.md) for boundaries and limitations.

## Behind the plugin

Abacus maintains the engineering guidance and Studio workflows. Skills provide
specialized playbooks, while Studio's MCP services supply authorized project
information and workflow access. Optional project tools add design guidance and
local code mapping without requiring clients to learn another set of commands.
A small local routing hook helps Claude choose the development workflow from a
normal request. It does not upload data, edit your project, or grant permissions.
Automatic selection is guidance, not a guarantee for every request or model.

For installation help, updates, or project access, contact your Abacus team.

[Installation and updates](INSTALL.md) ·
[Maintainer guide](references/maintainer-guide.md) ·
[Third-party acknowledgements](THIRD_PARTY_NOTICES.md)

By Abacus Internet Solutions Inc. See [LICENSE](LICENSE) for the current licensing
document, which is marked as a draft, not effective terms. Third-party components
retain their own applicable licenses.
