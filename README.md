# AI Factory

**A professional, AI-safe development lifecycle for any repository, set up by Claude Code.**

AI agents write code fast. Without a frame, that speed turns into untested changes, unreviewed merges and nobody knowing what is live. This skill gives Claude one job: install the frame on your project, end to end, and prove it works.

> The AI follows the routine. The pipeline enforces it.

## What it builds

- `main` as the single source of truth, locked by a GitHub ruleset with **no bypass**, not even for the owner
- pull requests only, with one required **Test** gate (build, tests, leaked-key scan) and a **PR title** check
- a Claude **AI review** on every pull request (advice, never blocking)
- **staging** that updates on every merge, then a **Promote to production** button that only listed people can press
- a check that each environment really runs the new commit, **dated release tags** (`v2026.12.15-1`) with release notes, and a **Rollback** button
- a **nightly AI security review** (Arcanum sec-context catalogue), weekly **Dependabot** updates, alerts when a pipeline run fails
- the Claude Code rules inside the repo: a `CLAUDE.md` section, a `/ship` routine, and a **hook** that blocks Claude from pushing to `main`, deploying from its session, starting the production buttons or weakening protection (35 tested cases)
- the method upstream: Spec Kit (or GSD Core for very long projects)

It works with any stack (Node, Python, Go and others) and any host: Cloudflare Workers and Pages, Railway, Vercel, Fly.io, Firebase, Modal, LiveKit Cloud, or a container on a server. Claude discovers the project first, proposes a plan, and stops only for what needs a person: payments, admin rights, secrets, and the production button.

## Install

**New to this? Follow the step-by-step guide:** [English](docs/INSTALL.md) | [Français](docs/INSTALL.fr.md). It covers every plan (Free, Pro, Max, Team, Enterprise), what an owner does and what a member does, first use on the web and on a phone, updates, and fixes for common problems.

### Claude Code in the terminal or an IDE

As a plugin, updated with the marketplace:

```
/plugin marketplace add vincentsider/ai-factory
/plugin install ai-factory@ai-factory
```

Or as a personal skill, available in every project on the machine:

```bash
curl -fsSL https://raw.githubusercontent.com/vincentsider/ai-factory/main/install.sh | bash -s -- --user
```

### Claude Code on the web (claude.ai/code)

**Option A, once for your account.** Download `ai-factory.zip` from the [latest release](https://github.com/vincentsider/ai-factory/releases/latest). On claude.ai: **Customize**, **Skills**, **+**, **Create skill**, **Upload a skill**, choose the zip. The skill is then available in your Claude Code sessions on the web.

On a Team or Enterprise plan, an owner must first allow skills: **Organization settings**, **Plugins & skills**, **Policy** tab, turn on **Cloud code execution and file creation** and **Skills**.

**Option B, inside one repository.** In a Claude Code session on the repository, ask:

> Run `curl -fsSL https://raw.githubusercontent.com/vincentsider/ai-factory/main/install.sh | bash` and open a pull request that adds `.claude/skills/ai-factory`.

## Use

In a Claude Code session on the project:

```
/ai-factory
```

or simply: *"Set up the AI factory pipeline on this repo."* Add a preference if you want: `/ai-factory lite` (no staging, for an internal tool), `/ai-factory library` (a package that is released, not deployed).

Claude works phase by phase, one pull request per phase: discovery and plan, prerequisites, rules and hook, the gate and the lock on `main`, AI review, staging and production, security, alerts, method, then a full drill (a real change to production, a rollback, and attempts to break the locks).

## What you will need

| Item | Cost (late 2026) |
|---|---|
| GitHub Pro (personal) or Team (organisation), for branch protection on private repos | about 4 dollars per user per month |
| GitHub Actions | about 2 cents per gate run; Pro and Team include about 3,000 minutes a month |
| A Claude subscription (Pro, Max, Team or Enterprise) | the review and the nightly review can run on it |
| Your host's staging environment | usually its smallest plan |
| Dependabot, gitleaks, Spec Kit, Arcanum sec-context | free |

## Safety by design

- Claude never deploys from its session: only GitHub Actions does, with tokens Claude never sees.
- Production is promoted by a person. The workflow refuses a commit that did not pass staging, and the hook stops Claude from starting it.
- Secrets go only into GitHub or the host, pasted by a person, never into files or the chat.
- Live keys found in git history are reported (never printed) for rotation.

## Repository layout

```
skills/ai-factory/SKILL.md      the skill (short, loads on use)
skills/ai-factory/reference/    one file per phase, read when needed
skills/ai-factory/templates/    workflows, hook, tests, ruleset, CLAUDE.md section
.claude-plugin/marketplace.json the plugin marketplace entry
install.sh, install-files.txt   the installer and its file list
tests/run.sh                    every check, locally and in CI
```

## Credits and licence

MIT licence, by Vincent Sider ([DeepBlocker.ai](https://deepblocker.ai)). Built from a production pipeline and the mistakes it made first.

The nightly security review uses [sec-context](https://github.com/Arcanum-Sec/sec-context) by Arcanum Information Security (CC BY 4.0). It is downloaded into your repository at setup, with attribution, not redistributed here.

---

## En français : installer sur Claude Code web (claude.ai)

**Guide complet pas à pas, pour les débutants : [docs/INSTALL.fr.md](docs/INSTALL.fr.md).** En résumé :

1. Téléchargez `ai-factory.zip` depuis la [dernière version](https://github.com/vincentsider/ai-factory/releases/latest).
2. Sur claude.ai : **Customize**, **Skills**, **+**, **Create skill**, **Upload a skill**, puis choisissez le fichier zip.
3. Offre Team ou Enterprise : un propriétaire de l'organisation doit d'abord autoriser les skills. **Organization settings**, **Plugins & skills**, onglet **Policy** : activer **Cloud code execution and file creation** et **Skills**.
4. Ouvrez une session sur claude.ai/code, sur le dépôt du projet, et écrivez : **/ai-factory** (ou « Mets en place le pipeline AI Factory sur ce dépôt »). Claude répond en français et vous guide à chaque étape où il a besoin de vous.
