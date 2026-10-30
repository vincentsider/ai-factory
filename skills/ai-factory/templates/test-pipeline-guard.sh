#!/usr/bin/env bash
# Tests for pipeline-guard.sh. Run: bash test-pipeline-guard.sh [path/to/pipeline-guard.sh]
# Builds a throwaway git repo, then feeds the hook one command at a time,
# exactly as Claude Code does (JSON on stdin), and checks the exit code:
# 2 = blocked, 0 = allowed. Prints a table and exits 1 if any case is wrong.
set -u
GUARD="${1:-.claude/hooks/pipeline-guard.sh}"
GUARD="$(cd "$(dirname "$GUARD")" && pwd)/$(basename "$GUARD")"
[ -x "$GUARD" ] || { echo "Not executable: $GUARD"; exit 1; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cd "$TMP" && git init -q -b main && git -c user.email=t@t -c user.name=t commit -q --allow-empty -m init

fail=0
check() { # expected-code command
  local want="$1" cmd="$2" got
  printf '%s' "$cmd" | python3 -c 'import json,sys;print(json.dumps({"tool_input":{"command":sys.stdin.read()}}))' \
    | "$GUARD" >/dev/null 2>&1
  got=$?
  if [ "$got" = "$want" ]; then mark=ok; else mark=WRONG; fail=1; fi
  printf '%-5s | want %s got %s | %s\n' "$mark" "$want" "$got" "$cmd"
}

echo "--- while on main"
check 2 "git push origin main"
check 2 "git push"
check 2 "git push origin HEAD"
check 2 "git push -u origin HEAD:main"
check 2 "git -C . push origin +main"
check 2 "npm test && git push origin main"
check 2 "git push --mirror origin"
check 0 "git push origin feat/x"

git switch -q -c feat/x
echo "--- while on feat/x"
check 0 "git push"
check 0 "git push -u origin feat/x"
check 0 "git push origin HEAD"
check 2 "git push origin refs/heads/main"
check 2 "gh workflow run promote-production.yml"
check 2 "gh workflow run rollback.yml -f tag=v2026.01.01-1"
check 0 "gh workflow run tests.yml"
check 2 "gh api -X POST repos/o/r/actions/workflows/promote-production.yml/dispatches -f ref=main"
check 2 "gh api repos/o/r/actions/runs/1/pending_deployments -f state=approved"
check 2 "npx wrangler deploy --env production"
check 0 "npx wrangler dev"
check 2 "npx wrangler d1 migrations apply db --remote"
check 0 "npx wrangler d1 migrations apply db --local"
check 2 "railway up --ci"
check 0 "railway logs"
check 2 "vercel --prod"
check 0 "vercel dev"
check 2 "flyctl deploy"
check 2 "firebase deploy --only hosting"
check 2 "modal deploy app.py"
check 2 "lk agent deploy"
check 2 "gh api -X DELETE repos/o/r/rulesets/1"
check 0 "gh api repos/o/r/rulesets"
check 0 "gh api -X POST repos/o/r/rulesets --input ruleset.json"
check 2 "echo hello; firebase deploy"
check 0 "git commit -m 'git push origin main'"
check 0 "npm test"

echo
if [ "$fail" = 0 ]; then echo "All cases behave as expected."; else echo "Some cases are WRONG."; exit 1; fi
