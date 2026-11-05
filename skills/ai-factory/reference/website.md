# Phase 8b: public website checks

Only when the project is a website anyone can visit (a shop, a tourism site, a marketing site). Skip for internal tools, APIs and libraries. Set the repository variable `PUBLIC_WEBSITE` to `true`; the checks then run after every staging update (in `deploy-staging.yml`) and after every production update (in `promote-production.yml`).

Explain them to the user in plain words:
- **Old addresses still work.** When a new site replaces an old one, every old link and every old Google result must lead to the right new page, not to an error page. This one **blocks**: if an old address breaks, staging turns red and "Promote to production" refuses that version.
- **What Google reads is still there.** Each key page keeps its title, its description (the text under the link in Google), its main heading, its language, its canonical address and its structured data. The site map and robots file exist. Any of these that changes or disappears since the previous update is reported. It **warns** at first.
- **Usable by everyone.** The key pages are opened in a real browser and tested against the accessibility rules (WCAG 2.1 A and AA, the base of the French RGAA), and the keyboard must be able to move through them. It **warns** at first. Automatic tests find only part of the problems: a human accessibility audit is still needed before going live, and the law may require one (RGAA for French public bodies).

## Set it up
1. Copy from `${CLAUDE_SKILL_DIR}/templates/` to `.github/scripts/`: `check-redirects.py`, `seo-check.py`, `a11y-check.mjs`.
2. Copy `key-pages.txt` and `redirects.csv` to `.github/website/` and fill them:
   - `key-pages.txt`: 5 to 15 paths that matter most (home, main sections, one page of each type, search, contact). Ask the user.
   - `redirects.csv`: one line per old address and the page it must lead to. Build it from the old site's sitemap and from Google Search Console (Pages report, HUMAN ACTION: an export). On a site that never had an old version, keep only the header line: the check then has nothing to verify and passes.
3. The site itself must serve those redirects as permanent ones (301 or 308), in one step. On Cloudflare Workers with static assets, a `_redirects` file handles up to about 2,000 fixed rules; beyond that, use Cloudflare Bulk Redirects. Keep redirects for at least a year.
4. Staging must not be indexed (`X-Robots-Tag: noindex` and a disallow-all robots.txt, Phase 8). The checks know this and do not flag it. Canonical addresses and site map entries must point to the production address (`PRODUCTION_URL`), even on staging.
5. Run the checks once by hand against staging, show the user the results, and fix or explain each problem.

## Later: make them block
When a warning check has been right for a few weeks, set `SEO_MODE` or `A11Y_MODE` to `block`. Before the launch of a new site, it is wise to set both to `block` for the last week, then decide.

## Before the switch-over of a site that replaces an old one
Add these to the launch checklist (`docs/cicd/launch.md`): 100% of old addresses pass; the human accessibility audit is done or booked; the new sitemap is ready to submit in Google Search Console on the day; the 20 most visited pages are checked by hand on production right after the switch; the old hosting is cancelled only after a week without problems.
