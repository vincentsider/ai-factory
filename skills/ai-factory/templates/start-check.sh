#!/usr/bin/env bash
# start-check.sh "BUILD_COMMAND" "START_COMMAND" [SECONDS]
# Builds the app exactly the way production does, then starts it with no
# settings for SECONDS (default 25) and fails only if a module cannot be
# found. Why: a build used only by CI can compile less than production does,
# so an import production cannot resolve passes every test and then crashes
# every release at start. Imports are resolved before any code runs, so a
# missing module always shows up before the expected "missing setting"
# errors, which do not fail this check.
# Recognised errors: Node (ERR_MODULE_NOT_FOUND, Cannot find module,
# ERR_UNSUPPORTED_DIR_IMPORT) and Python (ModuleNotFoundError, ImportError).
# Extra patterns: START_CHECK_PATTERNS (an extended regex, added with |).
set -uo pipefail
BUILD="${1:?build command, the same as production}"
START="${2:?start command, the same as production}"
SECS="${3:-25}"
PAT='ERR_MODULE_NOT_FOUND|Cannot find module|ERR_UNSUPPORTED_DIR_IMPORT|ModuleNotFoundError|ImportError: '
[ -n "${START_CHECK_PATTERNS:-}" ] && PAT="$PAT|$START_CHECK_PATTERNS"
LOG="${START_CHECK_LOG:-start.log}"

echo "Build: $BUILD"
bash -c "$BUILD" || { echo "::error::The production build itself failed."; exit 1; }

echo "Start for ${SECS}s: $START"
if command -v timeout >/dev/null; then
  PORT="${PORT:-0}" NODE_ENV="${NODE_ENV:-production}" timeout "$SECS" bash -c "$START" > "$LOG" 2>&1 || true
else
  PORT="${PORT:-0}" NODE_ENV="${NODE_ENV:-production}" bash -c "$START" > "$LOG" 2>&1 &
  pid=$!; sleep "$SECS"; kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null || true
fi

if grep -nE "$PAT" "$LOG"; then
  echo "::error::The built app cannot load a module (lines above). For Node ESM: a relative import probably lacks its .js ending."
  if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
    { echo "### The built app does not start: a module is missing"; echo '```'; grep -nE -A3 "$PAT" "$LOG" | head -40; echo '```'; } >> "$GITHUB_STEP_SUMMARY"
  fi
  exit 1
fi
echo "The built app loaded all its modules. First lines of its output:"
head -15 "$LOG"
