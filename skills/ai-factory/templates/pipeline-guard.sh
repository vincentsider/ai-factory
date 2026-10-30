#!/usr/bin/env bash
# PreToolUse hook (Bash). Blocks the shell commands that would let an AI
# session skip the pipeline. Exit 2 = the command is cancelled and the
# message is shown to Claude. Everything else exits 0.
#
#   1. git push that updates the protected branch (direct, HEAD:main, or a
#      bare push while on it), and force pushes to it.
#   2. Starting a production or rollback workflow, or approving a deployment.
#   3. Deploying from the session with a host CLI (only GitHub Actions deploys).
#   4. Weakening repository protection through the GitHub API.
#
# Tune the two lists below for the project. Keep them short and explicit.
PROTECTED_BRANCH="main"
# Workflow files a human must start (matched against `gh workflow run <x>`).
HUMAN_ONLY_WORKFLOWS='promote|production|rollback|release'

cmd=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
[ -z "$cmd" ] && exit 0

block() {
  echo "Blocked by .claude/hooks/pipeline-guard.sh: $1" >&2
  echo "$2" >&2
  exit 2
}
PR_HINT="Changes reach $PROTECTED_BRANCH only through a pull request: push a feat/ or fix/ branch and open a PR. See the /ship skill."

# Split chained commands (; && || | and newlines) and check each part.
parts=$(printf '%s\n' "$cmd" | sed -E 's/(&&|\|\||;|\|)/\
/g')
while IFS= read -r part; do
  p=$(echo "$part" | sed -E 's/^[[:space:]]+//')
  [ -z "$p" ] && continue

  # ---- 1. git push ----
  if echo "$p" | grep -Eq '^(sudo[[:space:]]+)?git([[:space:]]+-C[[:space:]]+[^[:space:]]+)?[[:space:]]+push([[:space:]]|$)'; then
    dir=$(echo "$p" | sed -nE 's/^git[[:space:]]+-C[[:space:]]+([^[:space:]]+).*/\1/p')
    args=$(echo "$p" | sed -E 's/^.*git([[:space:]]+-C[[:space:]]+[^[:space:]]+)?[[:space:]]+push//')
    for a in $args; do
      case "$a" in
        "$PROTECTED_BRANCH"|"+$PROTECTED_BRANCH"|*:"$PROTECTED_BRANCH"|*:refs/heads/"$PROTECTED_BRANCH"|refs/heads/"$PROTECTED_BRANCH")
          block "direct push to $PROTECTED_BRANCH." "$PR_HINT" ;;
        --mirror|--all) block "push $a would update $PROTECTED_BRANCH." "$PR_HINT" ;;
      esac
    done
    branch=$(git ${dir:+-C "$dir"} rev-parse --abbrev-ref HEAD 2>/dev/null)
    # shellcheck disable=SC2086 # word splitting is intended here
    refspecs=$(printf '%s\n' $args | grep -v '^-' | sed -n '2,$p')
    if [ "$branch" = "$PROTECTED_BRANCH" ]; then
      [ -z "$refspecs" ] && block "you are on $PROTECTED_BRANCH; this push would update it directly." "$PR_HINT"
      for r in $refspecs; do
        case "$r" in HEAD|+HEAD|@|+@) block "you are on $PROTECTED_BRANCH; pushing HEAD would update it directly." "$PR_HINT" ;; esac
      done
    fi
  fi

  # ---- 2. production / rollback workflows and deployment approvals ----
  if echo "$p" | grep -Eq '(^|[[:space:]])gh[[:space:]]+workflow[[:space:]]+run[[:space:]]'; then
    wf=$(echo "$p" | sed -E 's/.*gh[[:space:]]+workflow[[:space:]]+run[[:space:]]+//' | awk '{print $1}' | tr -d "\"'")
    echo "$wf" | grep -Eiq "$HUMAN_ONLY_WORKFLOWS" && \
      block "'$wf' is started by a person, not by Claude." "Tell the user staging is ready and which button to press (Actions, the workflow, Run workflow)."
  fi
  if echo "$p" | grep -Eq '/pending_deployments|/environments/[^/[:space:]]+/deployment-branch-policies'; then
    block "deployment approvals and environment rules are for people only." "Ask the user to approve or change it in GitHub."
  fi
  if echo "$p" | grep -Eq '/actions/workflows/[^/[:space:]]+/dispatches' && echo "$p" | grep -Eiq "$HUMAN_ONLY_WORKFLOWS"; then
    block "this would start a human-only workflow through the API." "Ask the user to press the button."
  fi

  # ---- 3. deploying from the session ----
  if echo "$p" | grep -Eq '(^|[[:space:]/])(npx[[:space:]]+|bunx[[:space:]]+|pnpm[[:space:]]+(dlx[[:space:]]+)?)?wrangler[[:space:]]+(deploy|publish|rollback|versions[[:space:]]+deploy|secret[[:space:]]+(put|delete|bulk))' \
     || echo "$p" | grep -Eq '(^|[[:space:]/])(npx[[:space:]]+)?wrangler[[:space:]]+d1[[:space:]].*--remote' \
     || echo "$p" | grep -Eq '(^|[[:space:]/])railway[[:space:]]+(up|redeploy|down|variables?[[:space:]]+(set|delete)|variable[[:space:]]+(set|delete))' \
     || echo "$p" | grep -Eq '(^|[[:space:]/])(npx[[:space:]]+)?vercel([[:space:]].*)?[[:space:]](--prod|deploy|promote|rollback)' \
     || echo "$p" | grep -Eq '(^|[[:space:]/])(fly|flyctl)[[:space:]]+(deploy|secrets[[:space:]]+(set|unset)|releases[[:space:]]+rollback)' \
     || echo "$p" | grep -Eq '(^|[[:space:]/])(npx[[:space:]]+)?(netlify|firebase)[[:space:]]+deploy' \
     || echo "$p" | grep -Eq '(^|[[:space:]/])modal[[:space:]]+deploy' \
     || echo "$p" | grep -Eq '(^|[[:space:]/])lk[[:space:]]+agent[[:space:]]+(deploy|rollback)'; then
    block "deploying from a Claude session." "Only GitHub Actions deploys. Merge through a PR; staging updates by itself, production is promoted by a person."
  fi

  # ---- 4. weakening repository protection ----
  if echo "$p" | grep -Eq '(^|[[:space:]])gh[[:space:]]+api' && echo "$p" | grep -Eq '/rulesets|/branches/[^/[:space:]]+/protection'; then
    if echo "$p" | grep -Eiq -- '(-X|--method)[[:space:]]*(DELETE|PUT|PATCH)'; then
      block "changing or removing branch protection." "Protection changes are made by a person in GitHub, Settings, Rules."
    fi
  fi
done <<< "$parts"
exit 0
