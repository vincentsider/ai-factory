# Phase 11: alerts and incidents

1. **A failure reaches a person.** The deploy templates already open or update one issue labelled `pipeline-failure` on failure. Add the same `alert` job to any other workflow that must not fail silently. GitHub notifies by email and in the mobile app. If the team uses Slack, also post there with an incoming webhook stored as a secret.
2. **Runtime errors:** turn on the host's logs (for example Cloudflare `"observability": { "enabled": true }`). Add Sentry when the project has users; the DSN goes into GitHub secrets and the host, with the environment set to staging or production.
3. **Scheduled jobs inside the app** (syncs, imports, crons) report their own failures the same way, so a broken nightly sync is not discovered days later.
4. Write `docs/cicd/incident.md`, one page: how to tell what is live, how to roll back (the button, then the host dashboard), who to tell, how to write a short post-mortem as an issue.

# Phase 12: the method upstream

The pipeline makes changes safe; the method makes requests clear.
- **Spec Kit** (GitHub, MIT) for most projects. Check the current install at https://github.com/github/spec-kit. As of late 2026: `uv tool install specify-cli`, then `specify init --here --integration claude` (the old `--ai claude` flag fails). Commands are skills with a hyphen: `/speckit-constitution`, `/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-taskstoissues`, `/speckit-implement`.
- Write the **constitution** with the user, one question at a time: quality rules (a test for every change, additive migrations), product rules (accessibility, SEO, privacy, data ownership), and "every change goes through the pipeline". Mirror its 5 most important rules in `CLAUDE.md`.
- **GSD Core** for very long projects (many phases, weeks of work): https://github.com/open-gsd/gsd-core, `npx @opengsd/gsd-core@latest`. Each phase gets a fresh agent, so quality does not decay over long sessions.
- One method per project, never both on the same piece of work.

# Phase 13: prove it, then document

1. **The drill.** A tiny real change (a line of copy, a footer version) goes through every step: branch, PR, gate, review, merge, staging verified, the person presses Promote, production verified, tag and release created. Then the person runs Rollback to the previous tag, and Promote again. Time each step in `docs/cicd/setup-log.md`.
2. **Try to break it.** Show that a push to `main` is blocked by the hook and refused by GitHub; a PR with a failing test cannot merge; Promote refuses a commit that is not on staging; the hook blocks `gh workflow run promote-production.yml` and this project's host deploy command.
3. **Write `docs/cicd/00-overview.md`**, the day-to-day guide in plain language: the short version in 7 lines; a table of every piece (where it lives, what it does, can it be skipped); how to promote; how to roll back; the secrets (names only); the costs.
4. **End it with a status checklist:** implemented (ticked), not yet (unticked), next steps in order. Be honest about gaps.
5. **Final message:** what is live now, what each of the two buttons does, what the user still has to do (rotate keys, buy a plan, enable a setting), and what is left.
