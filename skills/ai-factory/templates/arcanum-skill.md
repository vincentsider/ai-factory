---
name: arcanum
description: Security review of code against the Arcanum sec-context catalogue of 25+ anti-patterns typical of AI-written code. Use to find vulnerabilities, audit code, check a diff before merge, or run the nightly security review.
---

# Arcanum security review

Source: Arcanum Information Security, "sec-context" (https://github.com/Arcanum-Sec/sec-context), CC BY 4.0. See SOURCE.md.

1. Take the list of files or the diff to review. Read the changed code and its context: callers, auth and permission checks, where input comes from, where output goes.
2. Never read the reference files whole: they are very large. Grep `references/ANTI_PATTERNS_BREADTH.md` for the patterns relevant to what you see (for example: injection, path traversal, SSRF, XSS, auth, session, secrets, crypto, deserialization, mass assignment, IDOR, dependency confusion). Use `references/ANTI_PATTERNS_DEPTH.md` only for a pattern you found, to confirm and to write the fix.
3. Keep only issues that are exploitable, with a concrete attack path. Drop style issues and theory.
4. For each issue: file, line, severity (CRITICAL, HIGH, MEDIUM, LOW), why it is exploitable, the fix.
5. Never paste a secret value. Say "a live key in file X, line Y" instead.
6. End with a one-line verdict, and the files you reviewed and skipped.
