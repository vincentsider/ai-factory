# Phase 6: the gate, then the lock on `main`

## 6.1 One check command per deployable part
Give each part one entry point that runs, in order, what exists for its stack: install exact versions, typecheck, lint (only if the code is lint-clean today; otherwise record the gap), build, tests.
- Node: `npm ci`, then a `check` script, for example `tsc --noEmit && eslint . && npm run build && npm test`
- Python: `uv sync --frozen` (or `pip install -r requirements.txt`), then `ruff check . && pytest` (add `mypy` if configured)
- Go: `go vet ./... && go build ./... && go test ./...`
- Other stacks: the equivalent
A part with no tests gets a first real smoke test of its main path, so the gate tests something.

## 6.2 `.github/workflows/tests.yml`
Copy `${CLAUDE_SKILL_DIR}/templates/tests.yml` and adapt it:
- one job per part (copy the `app` job), with its setup action, cache and check command
- the `changes` job lists each part's paths; delete it if the repo has one part
- keep the `secrets-scan` job and the final aggregate job named exactly **`Test`**: it always reports, so it can be required even when a part's job is skipped. Requiring a path-filtered job directly blocks every unrelated PR.
- each stack's dependency audit (`npm audit`, `pip-audit`, `govulncheck`) stays report-only until the backlog is clear; making it blocking is its own PR later
- pin third-party actions to at least a major version

Open the PR, watch the run, show it green.

## 6.3 `.github/workflows/pr-title.yml`
Copy `${CLAUDE_SKILL_DIR}/templates/pr-title.yml`. Dependabot titles pass because its config uses the `chore(deps)` prefix (Phase 10).

## 6.4 Lock `main` with a ruleset
Only after `Test` and `PR title` have each reported at least once.
- Terminal: `gh api -X POST repos/{owner}/{repo}/rulesets --input "${CLAUDE_SKILL_DIR}/templates/ruleset-protect-main.json"`, then read it back with `gh api repos/{owner}/{repo}/rulesets`.
- Web: HUMAN ACTION, Settings, Rules, Rulesets, New branch ruleset, with the same content: active; bypass list empty; target the default branch; restrict deletions; block force pushes; require a pull request (0 approvals, squash only); require status checks `Test` and `PR title`, branches up to date.

Why:
- **No bypass, not even the owner.** Claude acts with the user's GitHub login, so an owner bypass would let any Claude session merge red code. In a real emergency the owner switches the ruleset off with one click and back on after.
- **0 required approvals** while one person works on the repo: GitHub never lets you approve your own PR. With two or more people, set it to 1; because Claude opens PRs under the user's login, the other person must approve. That is real human review.
- **Squash only**: one PR is one commit on `main`, and its title is the release-note line.

Repository merge settings (terminal: `gh api -X PATCH repos/{owner}/{repo} -F allow_merge_commit=false -F allow_rebase_merge=false -F allow_squash_merge=true -F delete_branch_on_merge=true`; web: HUMAN ACTION, Settings, General, Pull Requests).

Verify: from a scratch branch try `git push origin HEAD:main`. The hook must block it. Explain that GitHub would refuse it too.
