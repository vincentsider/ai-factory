---
name: ai-factory
description: Set up a professional, AI-safe development lifecycle on any repository, any stack, any host. Builds the whole pipeline - protected main, pull requests only, a required test gate, Claude review on every PR, staging, a human Promote to production button, post-deploy checks, dated release tags, rollback, nightly AI security review, Dependabot, alerts, and the Claude Code rules (CLAUDE.md, a blocking hook, a ship skill). Works in the terminal and in Claude Code on the web. Use when the user asks to set up CI/CD, a pipeline, an AI factory, branch protection, staging and production, or a professional development lifecycle for a project.
license: MIT
compatibility: Claude Code (terminal, IDE or claude.ai/code). Needs git and a GitHub repository; gh is used when available.
metadata:
  version: "1.0.0"
  author: Vincent Sider (DeepBlocker.ai)
  source: https://github.com/vincentsider/ai-factory
---

# AI Factory: a professional pipeline for AI-written code

**The AI follows the routine. The pipeline enforces it.** Anything that must never be skipped lives in GitHub settings, the workflows or a hook, never only in a written instruction.

You set the whole pipeline up yourself, phase by phase. You stop only at steps marked **HUMAN ACTION** (payments, admin rights, secrets, the production button) and say exactly what to click. If the user gave preferences when invoking the skill (for example `lite`, `library`, or a host name), apply them.

All files referenced below live in this skill's folder: `${CLAUDE_SKILL_DIR}`. Copy templates from there; never retype them.

## Standing rules (apply for the whole task, re-read after any summary)

**Talk**
- Reply in the user's language. Plain words, short sentences, no jargon. Explain an unavoidable technical word (branch, pull request, staging) in one sentence the first time.
- Never use em dashes or en dashes. Use a comma, a colon or a new sentence.
- Before every HUMAN ACTION: say what already works, what is left, then the one thing you need. One request at a time.

**Work**
- Do everything you can yourself. Ask a person only for what needs their account, their money or an admin right. Never paste a command for them to run unless it needs their own login on their own machine; then say why.
- Every change, this setup included, goes through a short branch and a pull request. Never commit to the default branch. One phase, or one coherent piece of a phase, per PR.
- Verify every step yourself (a command, an API read, a page that answers, a green run) and say how. If a check fails, say so with the error. Never claim something works that you did not see work.
- Never put a secret in a file, commit, PR, issue or message. People paste secrets into GitHub or the host.
- Never weaken a check to make it pass. A wrong check is fixed in its own PR, with the reason.
- You never deploy from your session and never start the promote or rollback workflows. Only GitHub Actions deploys; only people press the production buttons.
- If other sessions or people may work in the same folder, use a git worktree. Never checkout, stash or rebase in their folder; never push commits that are not yours.
- Log each finished phase in `docs/cicd/setup-log.md`: done, left, PR numbers. 3 to 5 lines.

**Know where you run**
- `CLAUDE_CODE_REMOTE=true` means Claude Code on the web. There: `gh pr` and `gh issue` fail (GraphQL is blocked), so use your built-in GitHub tools or `gh api repos/{owner}/{repo}/...`; you can push branches but not tags; you cannot change repository settings, so those become HUMAN ACTIONS with click-by-click steps; use a session with only this repository, or the repository hooks do not load.
- Otherwise you run in a terminal with the user's own `gh` login: change repository settings through `gh api` yourself, then show the result. Never bypass a protection once it is in place.

## The target: the path of every change

1. A clear request (a spec, Phase 12).
2. A short-lived branch, then a pull request into `main`.
3. The gate runs (required `Test` and `PR title` checks); Claude reviews (advice only).
4. Merge only when green. GitHub itself refuses otherwise, for everybody, owner included.
5. The merge deploys to staging by itself; the workflow checks staging runs that commit.
6. A person presses **Promote to production**. The same commit goes live, is verified, and is tagged `vYYYY.MM.DD-N` with release notes.
7. Every night Claude reviews the day's code for security issues; every week Dependabot proposes updates. Failures open an issue.
8. If production breaks: the **Rollback** button, then a fix through the same path.

| Where the rule lives | Can an AI session skip it? |
|---|---|
| `CLAUDE.md` | Yes, it can forget |
| A skill such as `/ship` | Yes, it can ignore it |
| The hook in `.claude/settings.json` | No, in any Claude session on the repo |
| GitHub ruleset, required checks, workflows | No, for nobody |

## Phases

Read each reference file when you reach its phase, not before. Open one PR per phase unless the phase says otherwise.

| Phase | What | Read |
|---|---|---|
| 1 | Explain the principle above to the user in 5 lines, in their words | this file |
| 2 | Discovery: stack, parts, hosts, branches, Actions health, secrets in history; pick a profile; ask for decisions | [reference/discovery.md](reference/discovery.md) |
| 3 | Prerequisites: GitHub plan, Actions minutes, Claude GitHub App, Claude auth for Actions, host tokens, key rotation | [reference/prerequisites.md](reference/prerequisites.md) |
| 4 | Make `main` the single source of truth, retire an old live branch | [reference/main-and-rules.md](reference/main-and-rules.md) |
| 5 | Claude rules in the repo: CLAUDE.md section, the hook (copy and test it), `/ship`, PR template | [reference/main-and-rules.md](reference/main-and-rules.md) |
| 6 | The gate (`tests.yml`, `pr-title.yml`), then the ruleset that locks `main` | [reference/gate.md](reference/gate.md) |
| 7 | AI review on every PR | [reference/review.md](reference/review.md) |
| 8 | Staging, Promote to production, verify, tag and release, rollback; host adapters | [reference/deploy.md](reference/deploy.md) |
| 9 | Versions and release notes (done by Phase 8; document it) | [reference/deploy.md](reference/deploy.md) |
| 10 | Arcanum security skill, nightly review, Dependabot | [reference/security.md](reference/security.md) |
| 11 | Alerts and the incident page | [reference/finish.md](reference/finish.md) |
| 12 | The method upstream: Spec Kit (or GSD Core for very long projects) | [reference/finish.md](reference/finish.md) |
| 13 | Prove it end to end, try to break it, write the guide and the status checklist | [reference/finish.md](reference/finish.md) |
| Always | Lessons from a production pipeline, costs | [reference/lessons.md](reference/lessons.md) |

## Templates in this skill

| Template | Goes to | Notes |
|---|---|---|
| `templates/pipeline-guard.sh` | `.claude/hooks/pipeline-guard.sh` | `chmod +x`. Tune only the two settings at the top |
| `templates/test-pipeline-guard.sh` | `.claude/hooks/test-pipeline-guard.sh` | Run it; paste the result table in the PR |
| `templates/settings.json` | merge into `.claude/settings.json` | Keep existing keys and hooks |
| `templates/claude-md-lifecycle.md` | a section of `CLAUDE.md` | Fill the placeholders |
| `templates/ship-skill.md` | `.claude/skills/ship/SKILL.md` | Fill the check command |
| `templates/pull_request_template.md` | `.github/pull_request_template.md` | |
| `templates/tests.yml` | `.github/workflows/tests.yml` | ADAPT jobs to the stack and parts |
| `templates/pr-title.yml` | `.github/workflows/pr-title.yml` | |
| `templates/ruleset-protect-main.json` | GitHub ruleset | Through `gh api` or by hand |
| `templates/claude-review.yml` | `.github/workflows/claude-review.yml` | Or managed Claude Code Review |
| `templates/verify-live.sh` | `.github/scripts/verify-live.sh` | Used by the three deploy workflows |
| `templates/deploy-staging.yml` | `.github/workflows/deploy-staging.yml` | ADAPT the HOST ADAPTER steps |
| `templates/promote-production.yml` | `.github/workflows/promote-production.yml` | ADAPT the HOST ADAPTER steps |
| `templates/rollback.yml` | `.github/workflows/rollback.yml` | ADAPT the HOST ADAPTER step |
| `templates/arcanum-skill.md` | `.claude/skills/arcanum/SKILL.md` | Plus the two reference docs, see security.md |
| `templates/nightly-security.yml` | `.github/workflows/nightly-security.yml` | Or a Claude routine on the web |
| `templates/dependabot.yml` | `.github/dependabot.yml` | One entry per part and ecosystem |

Every template marked ADAPT contains steps that say `ADAPT`. None may remain when you open the PR: search for `ADAPT` before pushing. Run `actionlint` on the workflows if it is available.

## Done means

The drill in Phase 13 passed on the real repo: a tiny change went from branch to production through every step, a rollback and a re-promote worked, a direct push to `main` was blocked by the hook and refused by GitHub, a red PR could not merge, and promote refused a commit that was not on staging. `docs/cicd/00-overview.md` exists with an honest status checklist. Tell the user what is live, what each button does, what they still have to do, and what is left.
