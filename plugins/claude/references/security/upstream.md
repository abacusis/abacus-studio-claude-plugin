# Provenance and scope

Abacus Security adapts focused source-review principles from https://github.com/cloudflare/security-audit-skill.

Reference revision: `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` (identified 2026-10-14). This is not the complete upstream skill. It does not include its multi-phase orchestration, schemas, validators, execution harness, or full audit reports. The adaptation preserves source-first analysis, independent verification, boundary-based findings, validation blockers, and the prohibition on live probes. Abacus deliberately disables target execution in this version rather than assuming an ordinary workspace or Supabase sandbox meets upstream isolation requirements.

Update through reviewed Abacus plugin releases, not upstream auto-installation. Cloudflare does not endorse or certify this adaptation.

## Upstream license

MIT License

Copyright (c) 2025-2026 Cloudflare, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
