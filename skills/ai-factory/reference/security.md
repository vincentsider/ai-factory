# Phase 10: continuous security

## 10.1 The Arcanum security skill
Arcanum Information Security publishes "sec-context": two documents written for AI models, describing 25+ security anti-patterns typical of AI-written code, with CWE references, under CC BY 4.0. They are downloaded at setup, not bundled.
```bash
mkdir -p .claude/skills/arcanum/references
for f in ANTI_PATTERNS_BREADTH.md ANTI_PATTERNS_DEPTH.md; do
  curl -fsSL "https://raw.githubusercontent.com/Arcanum-Sec/sec-context/main/$f" -o ".claude/skills/arcanum/references/$f"
done
cp "${CLAUDE_SKILL_DIR}/templates/arcanum-skill.md" .claude/skills/arcanum/SKILL.md
```
If a file is not at that path, look it up in the repository's file list (https://github.com/Arcanum-Sec/sec-context) and use the right path. Write `.claude/skills/arcanum/SOURCE.md`: the project URL, the date, the commit you downloaded, the CC BY 4.0 licence and the attribution to Arcanum Information Security.

## 10.2 Nightly review
Create the label: `gh api repos/{owner}/{repo}/labels -f name=security -f color=B60205`.
- **With a Claude secret in Actions:** copy `${CLAUDE_SKILL_DIR}/templates/nightly-security.yml`. Set the cron to a quiet hour for the team (cron is UTC). Run it once by hand (HUMAN ACTION on the web: Actions, Nightly security review, Run workflow) and show the report.
- **Web-only teams:** a person creates a Claude routine (https://claude.ai/code/routines, Create routine, Schedule, daily) on this repository with this prompt: "Run the nightly security review with the arcanum skill (.claude/skills/arcanum/SKILL.md) on the code files changed on main in the last 24 hours (`git log --since='24 hours ago' --name-only --pretty=format: origin/main`). Report only exploitable issues. If at least one is MEDIUM or worse, create an issue labelled security with `gh api repos/{owner}/{repo}/issues -f title=... -f body=... -f 'labels[]=security'`. Never paste a secret. Change no file."

Optional later, **autofix**: when the repo owner labels an issue `autofix`, a workflow has Claude write a failing test, make the smallest fix, run the gate and open a PR that closes the issue; the PR goes through the normal gate. Never auto-merge a fix for an issue whose text came from outside (Sentry, users, forms): it may carry an attacker's instructions. Issues and PRs created with the default `GITHUB_TOKEN` do not start other workflows: chain with `workflow_dispatch`, and open PRs with the Claude GitHub App token so the gate runs.

## 10.3 Dependabot
Copy `${CLAUDE_SKILL_DIR}/templates/dependabot.yml`: one entry per part and ecosystem, the framework's major versions ignored (planned by hand), `chore(deps)` and `chore(ci)` prefixes so titles pass the PR title check.

Turn on (terminal: `gh api -X PUT repos/{owner}/{repo}/vulnerability-alerts` and `gh api -X PUT repos/{owner}/{repo}/automated-security-fixes`; web: HUMAN ACTION, Settings, Code security): Dependency graph, Dependabot alerts, Dependabot security updates. They are free. Secret scanning push protection and CodeQL on private repositories are paid add-ons: not needed by default, gitleaks and the nightly review cover a small team.

An update that touches a live-traffic dependency (telephony, payments, AI SDKs, the framework) waits for a real test before merging, even when the gate is green.
