# Changes

## 1.1.1 (November 2026)

Fixes found while installing 1.1 on a real repository:
- "Tests added" flags deleted test files, and compares only the branch's own changes (from the merge base), not what main gained meanwhile.
- The accessibility check runs even when an earlier website check failed in block mode.
- The weekly audit: the report check, and `Docs/` excluded like `docs/`.
- The hook judges a bare `git push` in the folder of a preceding `cd`, so work in a git worktree is not wrongly blocked (2 new cases).
- security.md: check that `.gitignore` does not hide the installed skills.

## 1.1.0 (November 2026)

- **A test with every change.** The rule is now written in the project's `CLAUDE.md` and in the `/ship` routine: new behaviour gets a new test, a bug gets a test that reproduces it before the fix, no test is deleted or weakened to pass. Two new checks watch it: "Tests added" (a change to the code without a test is flagged, label `no-test-needed` for the rare exception) and coverage (the share of code covered by tests must not go down compared with main). Both warn at first and can be switched to blocking with one repository variable.
- **Public website checks** (new Phase 8b), after every staging and production update: old addresses must lead to the right page in one permanent redirect (blocks by default), what search engines read on key pages is checked and compared with the previous update (warns), accessibility is tested in a real browser with axe-core and the keyboard (warns).
- **Weekly in-depth security audit** with Cloudflare's security-audit skill, read-only, `quick` profile on the week's changes, capped at 20 agent calls by default. A confirmed problem opens an issue.
- **Outside skills at a fixed version.** Arcanum and security-audit are installed by `fetch-vendored.py` from `vendor-lock.json`: exact commit, every file checked against its sha256, a `SOURCE.md` with credit and licence.
- The live checks can reach a staging site protected by Cloudflare Access (service token secrets `STAGING_ACCESS_CLIENT_ID` and `STAGING_ACCESS_CLIENT_SECRET`).
- The Claude review now also flags deleted or weakened tests.

## 1.0.0 (October 2026)

First release.
