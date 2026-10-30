# Lessons from a production pipeline (do not repeat them)

These all happened on the pipeline this skill comes from.

- **Check that Actions can run before trusting a green-looking repo.** Tests there had not run for weeks: the free minutes were used up and every run died in seconds. Nobody noticed.
- **Production must deploy from `main`.** It deployed from an old side branch while `main` was more than a thousand commits behind.
- **No owner bypass on the ruleset.** Claude acts with the owner's login.
- **A required check must always report.** Path-filtered jobs get skipped; require only the aggregate `Test` job.
- **Dependabot PRs cannot read repository secrets.** Skip them in workflows that need secrets, or those workflows fail on every update.
- **Issues and PRs created with the default `GITHUB_TOKEN` do not start other workflows.** Chain with `workflow_dispatch`, or use the Claude GitHub App token.
- **Scheduled workflows start late.** A midnight run started more than two hours late. Review a time window ("the last 24 hours"), not "today".
- **A nightly job must always leave a report**, or a silent failure looks like a clean night.
- **The AI review catches what tests miss.** In its first days it found a library upgrade tested only against a fake of the library, a session shared by two users, and a check loose enough to match phone numbers. Keep it, but it is advice: only the gate blocks.
- **Framework major upgrades are planned by hand.** One silently broke every server WebSocket in production for weeks.
- **The version endpoint must report the commit**, never a package version, or the deploy check cannot tell what is live.
- **Live keys in old git history stay live until rotated.** Deleting the file does nothing.
- **Parallel AI sessions in one folder collide.** Use worktrees; never checkout or stash in a shared folder; never push someone else's commits.

# Costs for a typical project (late 2026, check before buying)

| Item | Cost |
|---|---|
| GitHub Pro (personal) or Team (organisation) | about 4 dollars per user per month |
| GitHub Actions | about 2 cents per gate run; Pro and Team include about 3,000 minutes a month |
| Claude review and nightly review | the Claude subscription with `CLAUDE_CODE_OAUTH_TOKEN`, or a few dollars a month with an API key |
| Staging environment | usually the host's smallest plan or usage-based |
| Dependabot, gitleaks, Spec Kit, Arcanum sec-context | free |
| Sentry | free plan to start |
