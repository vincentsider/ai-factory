---
name: ship
description: The standard way to get a change from this repo into production. Branch from main, check locally, open a PR into main, wait for the gate and the Claude review, merge, watch staging, then hand over to a person for the production button. Use whenever you are about to commit, push, open a PR, merge or deploy, or when the user says ship it, open a PR, merge this or deploy.
---

# Ship a change

1. Branch from fresh main. If other sessions work in this folder, use a worktree:
   `git fetch origin && git worktree add ../<repo>-<name> -b feat/<name> origin/main` (or fix/, chore/).
2. Write the test with the change. New behaviour: a new test. Changed behaviour: update the test. A bug: first a test that fails because of the bug, then the fix. Only a change that cannot be tested (copy, styling) skips this, with the reason in the PR and the label `no-test-needed`.
3. Check locally, same steps as the gate: `<check command>`. All green, coverage not lower than before.
4. Commit with a Conventional Commit message. The PR title becomes the release-note line: make it readable by a non-developer.
5. Push the branch. Open the PR into main with three headings: Why, What changed, How verified.
6. Wait for the `Test` and `PR title` checks (required). Read the warnings too: "Tests added", coverage, and on websites the search-engine and accessibility checks. Read the Claude review; fix real issues and push again. Never merge on red.
7. Squash-merge when green. The branch is deleted automatically.
8. Watch "Deploy to staging": staging must report the new commit, and on a website the old addresses, search-engine and accessibility checks must pass or only warn. Look at the page.
9. Tell the user staging is ready and that they can press Actions, "Promote to production", Run workflow. Never start it yourself.
10. After the promote run: confirm production reports the commit and the tag `vYYYY.MM.DD-N` exists.
11. If production breaks: ask the user to run "Rollback" with the previous tag, then fix forward with a new PR.

Emergency: same path, just fast. A fix/ branch, a PR, a green gate, merge, promote. If the gate itself is broken, the owner can switch the ruleset off in GitHub (Settings, Rules), merge, and switch it back on at once. Say so in the PR.
