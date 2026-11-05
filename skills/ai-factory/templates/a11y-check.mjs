// a11y-check.mjs PAGES_FILE BASE_URL
// Opens each key page in a real browser (Chromium, through Playwright) and:
//   1. runs axe-core with the WCAG 2.1 A and AA rules (RGAA 4 is built on WCAG 2.1),
//   2. checks the keyboard can move through the page (Tab reaches a link or button).
// Reports "serious" and "critical" problems. Automatic tools find only part of
// the problems: a human RGAA audit is still needed before going live.
// A11Y_MODE=warn (default) only warns; =block fails the check.
// Protected staging: CF_ACCESS_CLIENT_ID / CF_ACCESS_CLIENT_SECRET or EXTRA_HEADER.
// Needs: npm i --no-save playwright@1.64.1 @axe-core/playwright@4.14.0
//        npx playwright install --with-deps chromium
import { readFileSync, appendFileSync } from "node:fs";
import { chromium } from "playwright";
import { AxeBuilder } from "@axe-core/playwright";

const [pagesFile, baseArg] = process.argv.slice(2);
if (!pagesFile || !baseArg) {
  console.error("Usage: node a11y-check.mjs PAGES_FILE BASE_URL");
  process.exit(2);
}
const base = baseArg.replace(/\/$/, "");
const mode = process.env.A11Y_MODE || "warn";
const pages = readFileSync(pagesFile, "utf8").split("\n").map((l) => l.trim()).filter((l) => l && !l.startsWith("#"));

const headers = {};
if (process.env.CF_ACCESS_CLIENT_ID) {
  headers["CF-Access-Client-Id"] = process.env.CF_ACCESS_CLIENT_ID;
  headers["CF-Access-Client-Secret"] = process.env.CF_ACCESS_CLIENT_SECRET || "";
}
const extra = process.env.EXTRA_HEADER || "";
if (extra.includes(":")) {
  const i = extra.indexOf(":");
  headers[extra.slice(0, i).trim()] = extra.slice(i + 1).trim();
}

const browser = await chromium.launch();
const context = await browser.newContext({ extraHTTPHeaders: headers });
const rows = [];
let serious = 0;
for (const path of pages) {
  const url = base + (path.startsWith("/") ? path : "/" + path);
  const page = await context.newPage();
  try {
    const res = await page.goto(url, { waitUntil: "load", timeout: 30000 });
    if (!res || res.status() !== 200) {
      rows.push([path, `answers ${res ? res.status() : "nothing"}`]);
      serious++;
      continue;
    }
    const result = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
    for (const v of result.violations.filter((v) => v.impact === "serious" || v.impact === "critical")) {
      serious++;
      rows.push([path, `${v.impact}: ${v.help} (${v.nodes.length} place(s), rule ${v.id})`]);
    }
    let reached = false;
    for (let i = 0; i < 5 && !reached; i++) {
      await page.keyboard.press("Tab");
      reached = await page.evaluate(() => {
        const el = document.activeElement;
        return !!el && el !== document.body && ["A", "BUTTON", "INPUT", "SELECT", "TEXTAREA", "SUMMARY"].includes(el.tagName);
      });
    }
    if (!reached) {
      serious++;
      rows.push([path, "the keyboard (Tab key) does not reach any link or button"]);
    }
  } catch (e) {
    serious++;
    rows.push([path, `could not be checked: ${String(e.message || e).split("\n")[0]}`]);
  } finally {
    await page.close();
  }
}
await browser.close();

const lines = [`### Accessibility check: ${pages.length} pages, ${serious} serious problem(s)`];
if (rows.length) lines.push("", "| Page | Problem |", "|---|---|", ...rows.map(([p, m]) => `| \`${p}\` | ${m.replace(/\|/g, "/")} |`));
lines.push("", "Automatic checks find only part of the problems. A human RGAA audit is still needed before going live.");
const report = lines.join("\n");
console.log(report);
if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, report + "\n\n");
if (serious && mode === "block") {
  console.log("::error::Serious accessibility problems found.");
  process.exit(1);
}
if (serious) console.log("::warning::Serious accessibility problems found (warning only).");
