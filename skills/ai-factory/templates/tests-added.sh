#!/usr/bin/env bash
# tests-added.sh BASE_SHA HEAD_SHA
# Checks that a change to the code comes with a change to the tests.
# Code files: common source extensions, outside test folders. Test files:
# test folders and *.test.* / *.spec.* / *_test.* / test_*.py names.
# A pull request with only docs, config or content changes passes.
# TESTS_ADDED_MODE=warn (default) only warns; =block fails the check.
# A deleted test file is always flagged, even without a code change: the
# rule is never to delete or weaken a test to make the checks pass.
# The pull request label "no-test-needed" skips it (SKIP_TESTS_ADDED=true),
# for the rare change that truly cannot be tested; say why in the PR.
set -euo pipefail
BASE="${1:?base sha}"; HEAD="${2:?head sha}"
MODE="${TESTS_ADDED_MODE:-warn}"
if [ "${SKIP_TESTS_ADDED:-false}" = "true" ]; then
  echo "Skipped: the pull request has the label no-test-needed."; exit 0
fi
CODE_RE='\.(ts|tsx|js|jsx|mjs|cjs|astro|vue|svelte|py|go|rb|php|java|kt|rs|cs|swift)$'
TEST_RE='(^|/)(tests?|__tests__|spec|e2e)/|\.(test|spec)\.[A-Za-z]+$|_test\.(go|py)$|(^|/)test_[^/]*\.py$'
# Three dots: only what this branch changed since it left BASE, not what
# BASE gained meanwhile.
CHANGED=$(git diff --name-only --diff-filter=AMR "$BASE...$HEAD")
CODE=$(printf '%s\n' "$CHANGED" | grep -E "$CODE_RE" | grep -Ev "$TEST_RE" | grep -Ev '(^|/)(docs?|\.github|scripts)/|\.config\.[a-z]+$|\.d\.ts$' || true)
TESTS=$(printf '%s\n' "$CHANGED" | grep -E "$TEST_RE" || true)
DELETED=$(git diff --name-only --diff-filter=D "$BASE...$HEAD" | grep -E "$TEST_RE" || true)
if [ -n "$DELETED" ]; then
  DMSG="This change deletes test files: $(printf '%s' "$DELETED" | tr '\n' ' ' | cut -c1-300)"
  echo "$DMSG"
  [ -n "${GITHUB_STEP_SUMMARY:-}" ] && printf '### Tests deleted\n%s\n\nA test is only removed when the behaviour it tests is removed too. Say why in the PR.\n\n' "$DMSG" >> "$GITHUB_STEP_SUMMARY"
  if [ "$MODE" = "block" ]; then echo "::error::Test files deleted."; exit 1; fi
  echo "::warning::Test files deleted (warning only)."
fi
if [ -z "$CODE" ]; then echo "No code file changed: nothing to check."; exit 0; fi
if [ -n "$TESTS" ]; then
  echo "Code and tests both changed:"; printf '%s\n' "$TESTS" | sed 's/^/  /'; exit 0
fi
MSG="This change modifies code but no test: $(printf '%s' "$CODE" | tr '\n' ' ' | cut -c1-300)"
echo "$MSG"
[ -n "${GITHUB_STEP_SUMMARY:-}" ] && printf '### No test in this change\n%s\n\nEvery change comes with a test that proves it works.\n\n' "$MSG" >> "$GITHUB_STEP_SUMMARY"
if [ "$MODE" = "block" ]; then echo "::error::Code changed without a test."; exit 1; fi
echo "::warning::Code changed without a test (warning only)."
