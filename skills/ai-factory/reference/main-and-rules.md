# Phase 4: one source of truth, `main`

Skip if production already deploys from `main`.

1. Nothing may be lost: `main` must become exactly the live code, with the old history kept. If `main` is an ancestor of the live branch, open a PR from the live branch into `main` and merge it with a merge commit (not squash, this once). If the two have diverged, stop and show the user both sides before doing anything.
2. Set `main` as the default branch (terminal: `gh api -X PATCH repos/{owner}/{repo} -f default_branch=main`; web: HUMAN ACTION, Settings, General).
3. Point the host at `main` for now (Phase 8 later moves all deploys to Actions).
4. Make the old live branch read-only with a ruleset (restrict updates and deletions, no bypass). Add one line to `CLAUDE.md`: it is retired, since when.

# Phase 5: the Claude rules inside the repo (one PR)

1. **CLAUDE.md**: add the section from `${CLAUDE_SKILL_DIR}/templates/claude-md-lifecycle.md`, placeholders filled. Keep the whole file under about 200 lines, most important rules first. Create `CLAUDE.md` if missing, with a 5-line project summary above the section.
2. **The hook**:
   ```bash
   mkdir -p .claude/hooks
   cp "${CLAUDE_SKILL_DIR}/templates/pipeline-guard.sh" .claude/hooks/pipeline-guard.sh
   cp "${CLAUDE_SKILL_DIR}/templates/test-pipeline-guard.sh" .claude/hooks/test-pipeline-guard.sh
   chmod +x .claude/hooks/pipeline-guard.sh
   ```
   Merge `${CLAUDE_SKILL_DIR}/templates/settings.json` into `.claude/settings.json`, keeping existing keys and hooks.
   If the project's protected branch is not `main`, or its human-only workflows have other names, change only the two settings at the top of the hook, and add matching cases to the test script.
   Run `bash .claude/hooks/test-pipeline-guard.sh .claude/hooks/pipeline-guard.sh`. Every line must say `ok`. Paste the table in the PR.
   State the limits in the PR: the hook covers Claude Code sessions on this repo; a person in a terminal is stopped by GitHub's ruleset instead (Phase 6); the hook is against mistakes, the ruleset is the lock.
3. **The `/ship` skill**: copy `${CLAUDE_SKILL_DIR}/templates/ship-skill.md` to `.claude/skills/ship/SKILL.md`, fill the check command, add project-specific steps if any (for example a migration rule).
4. **PR template**: copy `${CLAUDE_SKILL_DIR}/templates/pull_request_template.md` to `.github/pull_request_template.md` and fill the check command. Add project-specific ticks if useful (for example "old URLs keep a redirect").
5. Title the PR `chore(claude): pipeline rules, push guard and ship routine`.
