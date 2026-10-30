# Phase 2: discovery (no code changes)

Write `docs/cicd/00-discovery.md`. Record each finding with its evidence (file path or command output).

1. **Where you run:** web or terminal (see the standing rules in SKILL.md).
2. **The repository:**
   - owner, owner type and visibility: `gh api repos/{owner}/{repo} --jq '.owner.type, .private, .default_branch'`
   - the owner's GitHub plan if readable (`gh api users/{owner} --jq .plan` for your own account, `gh api orgs/{org} --jq .plan` for an organisation you administer)
   - branches, and **which branch production actually deploys from** (host settings, workflow triggers, README). If it is not `main`, say so loudly: Phase 4 fixes it first.
   - how far `main` is from the live branch: `git rev-list --left-right --count main...<live>`
3. **GitHub Actions health:** `gh api "repos/{owner}/{repo}/actions/runs?per_page=20" --jq '.workflow_runs[] | [.name, .conclusion, .run_started_at, .updated_at] | @tsv'`. Runs that fail within seconds with no steps usually mean the account is out of Actions minutes or has a zero spending limit. Report it: the pipeline depends on Actions running.
4. **The deployable parts.** A repo often holds several. For each folder with its own manifest or deploy config, record:
   - stack and version: `package.json` and lockfile type, `pyproject.toml` / `requirements.txt` / `uv.lock`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`, `pom.xml` / `build.gradle`, `Dockerfile`, other
   - the commands that exist today: install, typecheck, lint, build, test. Run them and note what passes.
   - **the host**, from its config: `wrangler.toml` / `wrangler.jsonc` (Cloudflare Workers or Pages), `railway.json` / `railway.toml` (Railway), `vercel.json` / `.vercel/` (Vercel), `fly.toml` (Fly.io), `netlify.toml` (Netlify), `firebase.json` (Firebase), Modal app files (Modal), `livekit.toml` (LiveKit Cloud), a Dockerfile with no host (container, host to choose), nothing (a library or tool: released, not deployed)
   - how it deploys today: by hand, host auto-deploy from a branch, an existing workflow
   - its data stores (database, buckets, queues) and whether staging copies exist
   - whether it exposes a health or version endpoint
5. **What already exists:** `.github/workflows/`, `.github/dependabot.yml`, `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/`, the tests and how many pass today.
6. **Secrets in history:** run gitleaks over the full history, for example with the release binary: `gitleaks git --no-banner --redact --report-path /tmp/gitleaks.json .`. List findings by file, line and rule, **never the values**. Live keys found must be rotated by a person (Phase 3.6).
7. **Gaps** against the target in SKILL.md, as a short list.

## Choose a profile

- **Standard** (default): staging plus the Promote to production button. For anything with users, customers or data.
- **Lite**: no staging; `main` deploys to production after the gate, then verify, tag and rollback. Only for a personal or internal tool where a short outage harms nobody. Say why you chose it.
- **Library**: no deploy; the gate on every PR, a release workflow on a version tag that publishes the package.

## Propose the plan, then wait

In at most 15 lines: the profile, the host adapter per part (see deploy.md), what costs money (prerequisites.md), and **all the decisions you need, in one list**. Open a PR with only `docs/cicd/00-discovery.md`. Wait for the user's answers before Phase 3.
