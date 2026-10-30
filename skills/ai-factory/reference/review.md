# Phase 7: AI review on every pull request (advice, never blocking)

Pick one, based on Phase 3.4.

**A. Claude Code Action.** Copy `${CLAUDE_SKILL_DIR}/templates/claude-review.yml` to `.github/workflows/claude-review.yml`. Add a "Project rules for reviewers" list in `CLAUDE.md` if the project has rules worth checking (for example: every API route checks the user's workspace; imports end in `.js`). It skips drafts and bot PRs: Dependabot PRs cannot read repository secrets.

**B. Claude Code Review (managed, Team and Enterprise).** An organisation owner enables it for the repository at https://claude.ai/admin-settings/claude-code. Nothing to maintain. Put the review focus in `CLAUDE.md`: bugs, security, project rules, missing tests.

Either way the review is advice. Only the gate blocks. Verify: the review comments on the PR that adds it, or on the next one.
