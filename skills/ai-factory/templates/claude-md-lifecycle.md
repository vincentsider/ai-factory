## Development lifecycle (CI/CD)

- `main` is the only source of truth. Never commit or push to it directly: a hook blocks it and GitHub refuses it.
- Every change: a short branch (`feat/...`, `fix/...`, `chore/...`), then a pull request into `main`. Follow the `/ship` skill.
- **Every change comes with a test** that proves it works: new behaviour gets a new test, changed behaviour gets an updated test. For a bug, first write a test that fails because of the bug, then fix it, and the test passes. A change that truly cannot be tested (copy, styling) says why in the PR and gets the `no-test-needed` label.
- Never delete or weaken a test to make the gate pass. If a test is wrong, fix it in the same PR and explain why.
- Before pushing, run `<check command>`. It runs the same steps as the gate, including the tests.
- Never merge on a red gate. Never weaken a check to make it pass.
- PR titles are Conventional Commits (`feat(area): ...`, `fix(area): ...`): they become the release notes.
- You never deploy. A merge deploys to staging by itself. A person presses "Promote to production". Never start the promote or rollback workflows.
- Database changes are additive (expand, then contract), so a rollback of code is always safe.
- Live version: `<production URL><version path>` shows the running commit. The latest GitHub release is what is live.
- Details: `docs/cicd/00-overview.md`.
