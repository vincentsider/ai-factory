# Phase 3: prerequisites (HUMAN ACTIONS, guided by you)

Present only what this project needs, in this order. Tick each item when the user confirms it. Verify what you can.

## 3.1 A GitHub plan that can protect a private branch
Free private repositories cannot protect branches or require checks. Public repositories can, for free.
- Personal account: **GitHub Pro**, about 4 dollars a month (profile picture, Settings, Billing and plans, Upgrade).
- Organisation: **GitHub Team**, about 4 dollars per user per month (the organisation, Settings, Billing and plans, Upgrade).

On private repositories, "required reviewers" on deployment environments needs GitHub Enterprise. This skill does not need it: production is a button only listed people can run, Claude is blocked from it by the hook, and the workflow refuses a commit that did not pass staging.

## 3.2 GitHub Actions can run
Settings, Billing, Actions: minutes left this month, or a spending limit above zero. Pro and Team include about 3,000 Linux minutes a month; a typical gate costs about 2 US cents a run.

## 3.3 The Claude GitHub App
Needed on the web, and for review and autofix workflows: https://github.com/apps/claude, Configure, choose the account or organisation that owns the repo, select the repository. A repository transferred from a personal account to an organisation needs the app installed on the organisation. An organisation owner may have to approve it (organisation Settings, GitHub Apps).

## 3.4 Claude inside GitHub Actions
The review (Phase 7) and the nightly review (Phase 10) need one repository secret:
- `CLAUDE_CODE_OAUTH_TOKEN`: uses the Claude subscription. Created once with `claude setup-token` in a terminal, valid one year, reusable across repositories. Write its expiry date in `docs/cicd/setup-log.md`.
- or `ANTHROPIC_API_KEY`: pay per use, from https://platform.claude.com.

No terminal on the team? Use the web alternatives: **Claude Code Review** (Team and Enterprise; an owner enables it at https://claude.ai/admin-settings/claude-code) for PR reviews, and a **Claude routine** (https://claude.ai/code/routines) for the nightly review.

## 3.5 Host tokens, stored only in GitHub
Only GitHub Actions deploys. One token per host, smallest scope that works. The person pastes them in the repo: Settings, Secrets and variables, Actions, New repository secret. Never in the chat.

| Host | Token | Secrets |
|---|---|---|
| Cloudflare | My Profile, API Tokens, template "Edit Cloudflare Workers", plus Account D1 Edit if D1 is used; limited to the account and zone | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` |
| Railway | Project settings, Tokens, one project token per environment | `RAILWAY_TOKEN_STAGING`, `RAILWAY_TOKEN_PRODUCTION` |
| Vercel | Account settings, Tokens, scoped to the team | `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` |
| Fly.io | `fly tokens create deploy -a APP`, one per app | `FLY_API_TOKEN_STAGING`, `FLY_API_TOKEN_PRODUCTION` |
| Firebase | a service account with Hosting or Functions deploy rights, per project | `FIREBASE_SERVICE_ACCOUNT_STAGING`, `FIREBASE_SERVICE_ACCOUNT_PRODUCTION` |
| Modal | Settings, API tokens | `MODAL_TOKEN_ID`, `MODAL_TOKEN_SECRET` |
| LiveKit Cloud | project URL, API key and secret, per project | `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` (suffix per environment) |
| Package registry (library profile) | an automation or trusted-publishing token | `NPM_TOKEN`, `PYPI_API_TOKEN`, or trusted publishing with no secret |

Verify the names (never the values): `gh api repos/{owner}/{repo}/actions/secrets --jq '.secrets[].name'`. If you cannot read them, ask for a screenshot of the page.

Repository **variables** (same page, Variables tab):
- `STAGING_URL`, `PRODUCTION_URL`: base URLs of the web parts
- `VERSION_PATH`: the version endpoint path, default `/version.json`
- `PROD_DEPLOYERS`: the GitHub logins allowed to promote and roll back, comma separated

## 3.6 Live keys found in history
For each live key found in Phase 2, the person rotates it in the provider's dashboard and updates it in the host. You cannot do this. Track it as one GitHub issue with a checklist, without values.

## 3.7 Claude's environment on the web
claude.ai/code, Configure cloud environments: network access **Trusted** is enough. Put **no** deploy token in environment variables: everyone using the environment can read them, and you never deploy anyway. If you must read a host API to diagnose, the person adds a read-only key as a **network secret** limited to that API's domain.
