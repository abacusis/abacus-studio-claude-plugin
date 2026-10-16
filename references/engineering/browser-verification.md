# Local browser verification

Use automatically for an authorized visible implementation change, not for a
planning-only request. Browser execution and installation remain subject to the
host's permissions and the user's approval scope. No extra client slash command.

## Prefer an available host browser

Use the host's browser facility if it can open the session's current local preview,
interact within approved scope, capture screenshots, and expose images for actual
inspection. Do not assume it exists or install an arbitrary MCP server. Identify
the changed source and correct preview first; a healthy HTTP response alone is
not a render check. Never reuse an unrelated server or guess a port from memory.
The Builder's tool allowlist does not include host-specific browser MCP tools.
The coordinator can perform host-browser checks and pass findings back to Builder;
do not grant broad new tools or pretend the Builder used an unavailable browser.

Use an isolated browser/session. No personal browser profile, cookie/storage-state
import, credential reads, automatic account creation, or production login. For
authenticated screens, the user may sign in to an approved sandbox account using
an available interactive host browser. If that is unavailable, report the flow
blocked/not verified rather than requesting keys or pretending authentication.

Before opening even a local page, confirm the app uses authorized sandbox services.
A local server can call production or have server-side effects; browser network
filters do not sandbox the server. Review the requested navigation/interactions
and actual target with the coordinator. Never click destructive controls, submit
forms, send email, charge payments, or change records without specific approval.

## Managed fallback

If no suitable host browser is available, offer a pinned Python Playwright 1.64.0
runtime and Chromium download in the same local setup approval. This is separate
from app dependencies and modifies neither package.json nor global Python. Python
3.10+ is required. No sudo, OS package installation, or disabling browser security.
Unsupported/missing platform dependencies must be reported, not silently repaired.
Only the coordinator installs under explicit approval:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/studio_git.py" browser-install --project-id "<Studio ID>" --workspace "<verified workspace>" --approved`

Installation rechecks Studio/workspace authorization. Capture never auto-installs.
After the approved preview starts, run:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/studio_git.py" browser-verify --project-id "<Studio ID>" --workspace "<verified workspace>" --url "<current approved loopback URL>" --approved`

Pass reviewed JSON on stdin with safely quoted host input, not shell interpolation
of client text. Example plan (replace with actual criterion and selector):

```json
{
  "viewports": ["desktop", "mobile"],
  "checks": [
    {"criterion": "R1", "action": "visible", "selector": "h1"},
    {"criterion": "R1", "action": "text", "selector": "h1", "text": "Invoice overview"}
  ]
}
```

The fallback supports visible/text assertions and reviewed click/fill actions,
not arbitrary JavaScript or project-controlled Playwright configuration/scripts.
Clicks/fills need interactions_approved:true. Never pass credentials as fill values;
password inputs are unsupported. It uses fresh headless unauthenticated contexts;
it does not import login state or manage authentication.

Default network policy allows only the exact approved loopback origin and
GET/HEAD/OPTIONS. External resource origins must be explicitly reviewed sandbox
origins in allowed_origins (no paths or wildcards).
Supabase resource hosts must match Studio's configured sandbox project; unknown
projects are rejected even when named in the plan. Non-loopback resources require
HTTPS. The local preview's process identity is confirmed by the coordinator, not
proved by the capture helper; verify it belongs to this workspace/session.
Redirect navigation outside
the approved local origin, WebSockets, service workers, and browser downloads are
blocked. This may block Vite HMR or sandbox APIs; report it and use an approved
host browser if needed. Do not bypass blocked requests or disable protections.

Writes additionally require allow_writes:true and a write_approval description
of specific sandbox effects. Replaying writes in both viewports additionally
requires repeat_writes_approved:true, or choose one viewport. Broad setup approval
does not grant data-write approval. Browser requests can still trigger server-side
writes through GET; do not describe capture as risk-free or read-only by nature.

## Evidence and honest results

Capture the changed screen at desktop and mobile widths and exercise the relevant
accepted flow. Use actual text/visibility assertions, not screenshot existence as
a proxy for behavior. Separate UI observations from UX observations.

Evidence stays in Git-ignored .studio/browser-evidence/<run>/ with fresh image
paths and result.json. Never upload it to Studio or Git automatically. Screenshots
can contain sensitive sandbox information. Viewing images with the coding tool
can send their contents to its AI provider under the normal tool interaction.
Approve capture and avoid/mask sensitive content when using suitable host tools.
The fallback offers no automatic redaction, videos, or traces. Do not claim it does.

Read each PNG using an image-capable tool before claiming a visual check. The
helper returns captured, failed, or stale; captured is NOT a visual pass. Its
image_inspection field starts not_performed_by_helper. No image tool means not
visually verified. Keep the original capture result; report any later inspection
separately with who inspected it and which image was read.

Record criterion, actual action/assertion, viewport, source state, result, image
path, and remaining gaps. The helper records a filtered source fingerprint before
and after capture; changed source makes it stale. Environment/dependency/backend
changes are outside that fingerprint and still need review. Generic runtime or
console error counts and blocked requests are reported without raw secret-bearing
logs or response bodies. Missing browsers, failed checks, login requirements,
timeouts, or blocked resources must not become a passing result.

Use the existing correction limit, then return unresolved findings to the
coordinator. Builder evidence is not independent verification or publishing
approval. Verifier and UI Reviewer are now installed; the latter opens approved
screenshots itself but cannot capture or use a browser. UX Reviewer reads actual
flow evidence supplied by the coordinator or authorized verifier; it also cannot
operate a browser. Attribute actions to the actor who actually executed them.
