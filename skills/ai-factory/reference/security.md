# Phase 10: continuous security

## 10.1 Install the two security skills, at a fixed version
Two outside skills are installed into the project: **Arcanum** (catalogue of security mistakes typical of AI-written code, Arcanum Information Security, CC BY 4.0) for the nightly review, and **security-audit** (Cloudflare, MIT) for the weekly in-depth review. `templates/vendor-lock.json` lists each file with its exact commit and fingerprint (sha256). The script refuses any file that does not match, so nobody can change these skills behind our back.
```bash
mkdir -p .claude/skills/arcanum
python3 "${CLAUDE_SKILL_DIR}/templates/fetch-vendored.py" "${CLAUDE_SKILL_DIR}/templates/vendor-lock.json"
cp "${CLAUDE_SKILL_DIR}/templates/arcanum-skill.md" .claude/skills/arcanum/SKILL.md
```
Check that git will keep the files: `git check-ignore -v .claude/skills/security-audit/SKILL.md`. Some repositories ignore `.claude/skills/`; then add them with `git add -f .claude/skills/security-audit .claude/skills/arcanum`, and say so in the PR. It writes a `SOURCE.md` next to each skill (author, licence, commit, date): keep it, the licences require the credit. Never edit the downloaded files; to update them, update the lock file in ai-factory.

## 10.2 Nightly review
Create the label: `gh api repos/{owner}/{repo}/labels -f name=security -f color=B60205`.
- **With a Claude secret in Actions:** copy `${CLAUDE_SKILL_DIR}/templates/nightly-security.yml`. Set the cron to a quiet hour for the team (cron is UTC). Run it once by hand (HUMAN ACTION on the web: Actions, Nightly security review, Run workflow) and show the report.
- **Web-only teams:** a person creates a Claude routine (https://claude.ai/code/routines, Create routine, Schedule, daily) on this repository with this prompt: "Run the nightly security review with the arcanum skill (.claude/skills/arcanum/SKILL.md) on the code files changed on main in the last 24 hours (`git log --since='24 hours ago' --name-only --pretty=format: origin/main`). Report only exploitable issues. If at least one is MEDIUM or worse, create an issue labelled security with `gh api repos/{owner}/{repo}/issues -f title=... -f body=... -f 'labels[]=security'`. Never paste a secret. Change no file."

## 10.4 Weekly in-depth audit
Copy `${CLAUDE_SKILL_DIR}/templates/weekly-security-audit.yml` to `.github/workflows/`. Once a week (Monday 02:00 UTC), Claude runs Cloudflare's security-audit skill on the week's changes, in its `quick` profile, read-only (it never runs the project's code), capped at `AUDIT_BUDGET` agent calls (default 20). It is stricter than the nightly review: a problem only counts if it names who attacks, which protection they get past and what harm follows, and a separate agent must fail to disprove it. So it raises few alarms, and they are worth reading. A confirmed problem of medium severity or worse opens an issue labelled `security`; the full report stays as a run artifact for 30 days.

Explain to the user in plain words: the nightly review is a quick check against a list of known mistakes; the weekly audit is a slower, deeper investigation of the week's changes. Both only report: neither changes code or blocks a change.

HUMAN ACTION on the web, yourself in the terminal: run it once by hand (Actions, Weekly security audit, Run workflow, since "30 days ago") and show the result and how long it took. If the runs take too long or cost too much, lower `AUDIT_BUDGET` (repository variable).

## 10.5 Optional later: autofix
Optional later, **autofix**: when the repo owner labels an issue `autofix`, a workflow has Claude write a failing test, make the smallest fix, run the gate and open a PR that closes the issue; the PR goes through the normal gate. Never auto-merge a fix for an issue whose text came from outside (Sentry, users, forms): it may carry an attacker's instructions. Issues and PRs created with the default `GITHUB_TOKEN` do not start other workflows: chain with `workflow_dispatch`, and open PRs with the Claude GitHub App token so the gate runs.

## 10.3 Dependabot
Copy `${CLAUDE_SKILL_DIR}/templates/dependabot.yml`: one entry per part and ecosystem, the framework's major versions ignored (planned by hand), `chore(deps)` and `chore(ci)` prefixes so titles pass the PR title check.

Turn on (terminal: `gh api -X PUT repos/{owner}/{repo}/vulnerability-alerts` and `gh api -X PUT repos/{owner}/{repo}/automated-security-fixes`; web: HUMAN ACTION, Settings, Code security): Dependency graph, Dependabot alerts, Dependabot security updates. They are free. Secret scanning push protection and CodeQL on private repositories are paid add-ons: not needed by default, gitleaks and the nightly review cover a small team.

An update that touches a live-traffic dependency (telephony, payments, AI SDKs, the framework) waits for a real test before merging, even when the gate is green.
