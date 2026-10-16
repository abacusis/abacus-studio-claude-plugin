# Evidence-led debugging

Start with the exact symptom, expected behavior, environment, and recent relevant changes. Redact credentials, authorization headers, private customer records, and sensitive artifacts before sharing output.

Build a repeatable failure signal using a focused test, request, browser interaction, or small harness. Confirm it exercises the reported bug rather than an unrelated error. For intermittent failures, record frequency and control nondeterministic inputs where practical.

Minimize the reproduction without removing what triggers it. Rank plausible causes and name observations that would confirm or refute each. Inspect or instrument the relevant boundaries; change one causal variable at a time. Avoid broad logging and speculative fixes.

Make the smallest justified fix, add an appropriate regression test, and rerun both the original reproduction and relevant checks. Remove temporary instrumentation created for this diagnosis without deleting user-owned artifacts.

If reproduction needs unavailable access, stop guessing: report what evidence is missing and request a safe, redacted artifact or authorized sandbox access. Do not add production instrumentation without separate authorization. Report diagnosis separately from remediation when the user requested diagnosis only.
