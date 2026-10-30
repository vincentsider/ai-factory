# Phase 8: staging, production, verify, tag, rollback

## 8.1 The contract every deployable part meets
1. **Two environments**, staging and production, each with its **own data store** and its own secrets. Staging never touches production data and never sends real email, SMS, calls or payments (test keys, allow-lists).
2. **A version endpoint** returning JSON with a `version` field equal to the running commit's short SHA: `/version.json` for a static site, `/api/health` for an app (set `VERSION_PATH`). The build writes it from `GITHUB_SHA`. It must report the commit, never a package version.
3. **Only GitHub Actions deploys**, with the host token. Turn off any host auto-deploy that skips the gate (a host that "waits for CI" before deploying `main` to staging is acceptable).
4. **Staging is not public**: `X-Robots-Tag: noindex` and a disallow-all `robots.txt`, plus access protection where the host has it (Cloudflare Access, Vercel deployment protection, basic auth).
5. **Database changes are additive** (expand, then contract): the new code works with the old schema and the old code with the new one, so a code rollback is always safe. Migrations run in the pipeline, staging first.

## 8.2 The three workflows
Copy from `${CLAUDE_SKILL_DIR}/templates/`:
- `verify-live.sh` to `.github/scripts/verify-live.sh` (`chmod +x`)
- `deploy-staging.yml`: every push to `main` reruns the gate (it calls `tests.yml`), migrates and deploys staging, verifies staging runs the commit, writes a summary with the next step
- `promote-production.yml`: run by a person from `main`; checks the person is in `PROD_DEPLOYERS`, that "Deploy to staging" succeeded for this commit and that staging runs it; then records the restore point, migrates, deploys, verifies, tags `vYYYY.MM.DD-N` and creates the release with notes from the PR titles
- `rollback.yml`: run by a person with a release tag; same person check; deploys that tag, verifies; never rolls back data

Replace every step marked `ADAPT` with the host adapter (8.4). Search for `ADAPT` before pushing; run `actionlint` if available. Create the `pipeline-failure` label (`gh api repos/{owner}/{repo}/labels -f name=pipeline-failure -f color=D93F0B`).

HUMAN ACTION: Settings, Environments: `staging` (no rules) and `production` (Deployment branches and tags: Selected, `main` only; on a public or Enterprise repo also add Required reviewers for a real approval click). Put host secrets that differ per environment as environment secrets.

**Lite profile:** no staging workflow. Rename `promote-production.yml` to `deploy-production.yml`, trigger it on `push` to `main` with a first job `test: uses: ./.github/workflows/tests.yml`, and drop the staging checks from `guard` (keep it from `main`). Keep `rollback.yml`.

**Library profile:** no deploy. A `release.yml` on pushed tags `v*`: runs the gate, builds, publishes with the registry token or trusted publishing, creates the GitHub release with notes.

## 8.3 Several deployable parts
Each part meets the contract. Keep one staging workflow and one promote workflow with one job per part (path-filtered on staging, all parts on promote), so a person presses one button. Give each web part its own URL variables (`STAGING_URL_API`, ...). A part that carries live traffic (calls, payments) may keep its own deploy workflow with a freeze switch: when the repository variable `PART_DEPLOY_FREEZE` is `true`, automatic runs skip with a clear message, manual runs still deploy.

## 8.4 Host adapters (the ADAPT steps only)
Use the host's official action or CLI in the workflow, never from your session. Check the current major versions of the actions when you write them.

| Host | Staging and production | Deploy step | Native rollback |
|---|---|---|---|
| Cloudflare Workers (incl. Astro, static assets) | `env.staging` and `env.production` in `wrangler.jsonc`: own worker names, routes, D1/R2/KV bindings and vars per env (bindings are not inherited) | `cloudflare/wrangler-action` with `apiToken`, `accountId`, `command: deploy --env staging` (or `production`); migrations `d1 migrations apply DB --remote --env ENV`; worker secrets through its `secrets:` input. Restore point: `d1 time-travel info DB` | `wrangler rollback` (code), D1 Time Travel (data) |
| Cloudflare Pages | a preview branch for staging, the production branch | `wrangler pages deploy DIR --project-name P --branch staging` or `--branch main` | dashboard, previous deployment |
| Railway | two environments in one project (duplicate one), own variables and data services | staging: auto-deploy `main` with "Wait for CI" on, or `railway up --service S --environment staging --ci`; production: auto-deploy off, `railway up --service S --environment production --ci` with its token | dashboard, Deployments, previous, Redeploy |
| Vercel | Preview for staging, Production for prod; disable automatic production deploys from git | `vercel pull --yes --environment=preview`, `vercel build`, `vercel deploy --prebuilt`; production with `--prod` | `vercel rollback`, or `vercel promote URL` |
| Fly.io | two apps, `APP-staging` and `APP` | `superfly/flyctl-actions/setup-flyctl`, then `flyctl deploy --app APP --remote-only` | `flyctl releases`, redeploy the previous image |
| Firebase Hosting or Functions | two Firebase projects | `firebase deploy --project ID --only hosting` (or functions) with the service account, or `FirebaseExtended/action-hosting-deploy` with `channelId: live` | Hosting release history |
| Modal | two Modal environments | `modal deploy --env staging` / `--env main` with the token secrets | redeploy the previous tag |
| LiveKit Cloud agents | two LiveKit projects | `lk agent deploy` with the project URL, key and secret; health-check the new version, roll back automatically if unhealthy | `lk agent rollback` (paid plan) or redeploy the previous tag |
| Container on a server | two stacks or two hosts | build and push the image to GHCR tagged with the SHA, deploy that tag over SSH with a restricted deploy key | redeploy the previous image tag |

A host not listed: apply the contract with its official CLI, and record the choice and the reason in `docs/cicd/00-discovery.md`.

Also write `docs/cicd/rollback.md`: the rollback button, the host's instant dashboard rollback for emergencies (then regularise with the button or a fix PR), and the data-restore procedure for this host.

# Phase 9: versions and release notes
Phase 8 already tags every production deploy `vYYYY.MM.DD-N` with a GitHub Release built from the squash-merged PR titles. Write in `docs/cicd/00-overview.md`: "What is live? The latest release, and the version endpoint."
