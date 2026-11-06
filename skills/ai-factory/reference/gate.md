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

## 6.3 Every change comes with a test
This is a rule in `CLAUDE.md` and in `/ship` (Phase 5), and two checks in `tests.yml` watch it:
- **"Tests added"** (job in `tests.yml`, script `tests-added.sh`): a pull request that changes code without changing any test is flagged. Copy `${CLAUDE_SKILL_DIR}/templates/tests-added.sh` to `.github/scripts/tests-added.sh`. Create the label `no-test-needed` (`gh api repos/{owner}/{repo}/labels -f name=no-test-needed -f color=C5DEF5`) for the rare change that truly cannot be tested; the reason goes in the PR. Adjust the code and test patterns at the top of the script if the project names tests differently.
- **Coverage** (steps in the part's job, script `coverage-check.py`): the share of code covered by tests must not go down compared with main. Copy `${CLAUDE_SKILL_DIR}/templates/coverage-check.py` to `.github/scripts/coverage-check.py`. Add a coverage command per part and point `COVERAGE_REPORT` at its file:
  - Vitest: `vitest run --coverage --coverage.reporter=json-summary` -> `coverage/coverage-summary.json` (needs `@vitest/coverage-v8`)
  - Jest: `jest --coverage --coverageReporters=json-summary` -> `coverage/coverage-summary.json`
  - Python: `pytest --cov --cov-report=json` -> `coverage.json`
  - Go: `go test -coverprofile=cover.out ./... && go tool cover -func=cover.out > cover.txt` -> `cover.txt`
  - anything with an lcov or Cobertura report works too
  After each merge, main keeps its share as the reference (artifact `coverage-reference`). The first pull request after setup has no reference yet; that is normal.

**Warn or block.** Both checks only warn at first, because a new check can raise false alarms and non-technical users must never be stuck on noise. Explain this to the user in one sentence. When the check has been right for a few weeks, set the repository variable `TESTS_ADDED_MODE` or `COVERAGE_MODE` to `block` (Settings, Secrets and variables, Actions, Variables): from then on, the change cannot go in until it has its test. Write this next step in `docs/cicd/00-overview.md`.

Also check the existing tests are real: a part whose tests only use fakes of the code they claim to test, or that has no test at all, gets a first test of its main path before the gate is required.

## 6.4 `.github/workflows/pr-title.yml`
Copy `${CLAUDE_SKILL_DIR}/templates/pr-title.yml`. Dependabot titles pass because its config uses the `chore(deps)` prefix (Phase 10).

## 6.5 Lock `main` with a ruleset
Only after `Test` and `PR title` have each reported at least once.
- Terminal: `gh api -X POST repos/{owner}/{repo}/rulesets --input "${CLAUDE_SKILL_DIR}/templates/ruleset-protect-main.json"`, then read it back with `gh api repos/{owner}/{repo}/rulesets`.
- Web: HUMAN ACTION, Settings, Rules, Rulesets, New branch ruleset, with the same content: active; bypass list empty; target the default branch; restrict deletions; block force pushes; require a pull request (0 approvals, squash only); require status checks `Test` and `PR title`, branches up to date.

Why:
- **No bypass, not even the owner.** Claude acts with the user's GitHub login, so an owner bypass would let any Claude session merge red code. In a real emergency the owner switches the ruleset off with one click and back on after.
- **0 required approvals: the normal setting.** Most projects have one person, and GitHub never lets you approve your own pull request, so a required approval would block everything. The gate and the Claude review do the checking. Only if a second person joins the project later can it be raised to 1 (then, since Claude opens pull requests under its user's login, the other person approves). Never ask a solo user for a second reviewer.
- **Squash only**: one PR is one commit on `main`, and its title is the release-note line.

Repository merge settings (terminal: `gh api -X PATCH repos/{owner}/{repo} -F allow_merge_commit=false -F allow_rebase_merge=false -F allow_squash_merge=true -F delete_branch_on_merge=true`; web: HUMAN ACTION, Settings, General, Pull Requests).

Verify: from a scratch branch try `git push origin HEAD:main`. The hook must block it. Explain that GitHub would refuse it too.
