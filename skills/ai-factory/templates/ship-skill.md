---
name: ship
description: The standard way to get a change from this repo into production. Branch from main, check locally, open a PR into main, wait for the gate and the Claude review, merge, watch staging, then hand over to a person for the production button. Use whenever you are about to commit, push, open a PR, merge or deploy, or when the user says ship it, open a PR, merge this or deploy.
---

# Ship a change

1. Branch from fresh main. If other sessions work in this folder, use a worktree:
   `git fetch origin && git worktree add ../<repo>-<name> -b feat/<name> origin/main` (or fix/, chore/).
2. Check locally, same steps as the gate: `<check command>`. All green.
3. Commit with a Conventional Commit message. The PR title becomes the release-note line: make it readable by a non-developer.
4. Push the branch. Open the PR into main with three headings: Why, What changed, How verified.
5. Wait for the `Test` and `PR title` checks (required). Read the Claude review; fix real issues and push again. Never merge on red.
6. Squash-merge when green. The branch is deleted automatically.
7. Watch "Deploy to staging": staging must report the new commit. Look at the page.
8. Tell the user staging is ready and that they can press Actions, "Promote to production", Run workflow. Never start it yourself.
9. After the promote run: confirm production reports the commit and the tag `vYYYY.MM.DD-N` exists.
10. If production breaks: ask the user to run "Rollback" with the previous tag, then fix forward with a new PR.

Emergency: same path, just fast. A fix/ branch, a PR, a green gate, merge, promote. If the gate itself is broken, the owner can switch the ruleset off in GitHub (Settings, Rules), merge, and switch it back on at once. Say so in the PR.
