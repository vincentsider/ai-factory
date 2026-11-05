#!/usr/bin/env python3
"""Check what Google and AI search engines read on a website's key pages.

For each page listed in PAGES_FILE (one path per line, # for comments):
  - the page answers 200 and declares its language (<html lang>),
  - it has a title and a description (what Google shows in its results),
  - it has exactly one main heading (<h1>),
  - its canonical address points to the production site, not to staging,
  - every language version it announces (hreflang) exists,
  - its structured data (JSON-LD, schema.org) is valid JSON.
Also: /robots.txt exists, /sitemap.xml exists and lists production addresses.
Drift: with a previous snapshot, it reports titles, descriptions, canonicals,
headings, languages or structured data that changed or disappeared.

Usage: python3 seo-check.py PAGES_FILE BASE_URL [--previous old.json] [--snapshot new.json]
Env: PRODUCTION_URL (for canonical and sitemap checks), SEO_MODE=warn (default)
or block, CF_ACCESS_CLIENT_ID / CF_ACCESS_CLIENT_SECRET or EXTRA_HEADER for a
protected staging site. A report is added to $GITHUB_STEP_SUMMARY when set.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


def headers():
    h = {"User-Agent": "ai-factory-checks/1.1"}
    if os.environ.get("CF_ACCESS_CLIENT_ID"):
        h["CF-Access-Client-Id"] = os.environ["CF_ACCESS_CLIENT_ID"]
        h["CF-Access-Client-Secret"] = os.environ.get("CF_ACCESS_CLIENT_SECRET", "")
    extra = os.environ.get("EXTRA_HEADER", "")
    if ":" in extra:
        k, v = extra.split(":", 1)
        h[k.strip()] = v.strip()
    return h


def get(url):
    req = urllib.request.Request(url, headers=headers())
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except (urllib.error.URLError, TimeoutError, OSError):
        return None, ""


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self.description = None
        self.canonical = None
        self.h1 = []
        self.hreflang = {}
        self.jsonld = []
        self._in = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang") or None
        elif tag == "meta" and a.get("name", "").lower() == "description":
            self.description = a.get("content", "").strip()
        elif tag == "link":
            rel = a.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonical = a.get("href")
            if "alternate" in rel and a.get("hreflang"):
                self.hreflang[a["hreflang"]] = a.get("href", "")
        elif tag in ("title", "h1") or (tag == "script" and a.get("type", "").lower() == "application/ld+json"):
            self._in = "jsonld" if tag == "script" else tag
            self._buf = []

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._in and (tag == self._in or (tag == "script" and self._in == "jsonld")):
            text = "".join(self._buf).strip()
            if self._in == "title":
                self.title = " ".join(text.split())
            elif self._in == "h1":
                self.h1.append(" ".join(text.split()))
            else:
                self.jsonld.append(text)
            self._in = None


def jsonld_types(blocks):
    types, bad = [], 0
    for b in blocks:
        try:
            data = json.loads(b)
        except ValueError:
            bad += 1
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        for it in items:
            t = it.get("@type") if isinstance(it, dict) else None
            types += t if isinstance(t, list) else [t] if t else []
    return sorted(set(types)), bad


def on_base(url, base):
    p = urllib.parse.urlsplit(url)
    b = urllib.parse.urlsplit(base)
    return urllib.parse.urlunsplit((b.scheme, b.netloc, p.path or "/", p.query, ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages_file")
    ap.add_argument("base_url")
    ap.add_argument("--previous")
    ap.add_argument("--snapshot")
    args = ap.parse_args()
    base = args.base_url.rstrip("/")
    prod = os.environ.get("PRODUCTION_URL", "").rstrip("/")
    prod_host = urllib.parse.urlsplit(prod).netloc if prod else ""
    mode = os.environ.get("SEO_MODE", "warn")
    pages = [l.strip() for l in open(args.pages_file, encoding="utf-8") if l.strip() and not l.strip().startswith("#")]

    problems, snapshot = [], {}
    for path in pages:
        url = base + (path if path.startswith("/") else "/" + path)
        status, html = get(url)
        if status != 200:
            problems.append((path, f"answers {status}" if status else "cannot be reached"))
            continue
        p = Page()
        p.feed(html)
        types, bad_jsonld = jsonld_types(p.jsonld)
        snapshot[path] = {"title": p.title, "description": p.description, "canonical": p.canonical,
                          "h1": p.h1, "lang": p.lang, "hreflang": sorted(p.hreflang), "jsonld": types}
        if not p.lang:
            problems.append((path, "the page does not declare its language (<html lang>)"))
        if not p.title:
            problems.append((path, "no title"))
        if not p.description:
            problems.append((path, "no description (meta description)"))
        if len(p.h1) != 1:
            problems.append((path, f"{len(p.h1)} main headings (h1), expected exactly 1"))
        if not p.canonical:
            problems.append((path, "no canonical address"))
        elif prod_host and urllib.parse.urlsplit(urllib.parse.urljoin(url, p.canonical)).netloc not in (prod_host, ""):
            problems.append((path, f"the canonical address points to {p.canonical}, not to the production site"))
        for lang, href in p.hreflang.items():
            s, _ = get(on_base(urllib.parse.urljoin(url, href), base))
            if s != 200:
                problems.append((path, f"the {lang} version ({href}) answers {s}"))
        if bad_jsonld:
            problems.append((path, f"{bad_jsonld} structured data block(s) are not valid JSON"))

    s, robots = get(base + "/robots.txt")
    if s != 200:
        problems.append(("/robots.txt", f"answers {s}"))
    s, sm = get(base + "/sitemap.xml")
    if s != 200:
        s, sm = get(base + "/sitemap-index.xml")
    if s != 200:
        problems.append(("/sitemap.xml", "no site map found (sitemap.xml or sitemap-index.xml)"))
    else:
        try:
            locs = [e.text.strip() for e in ET.fromstring(sm).iter() if e.tag.endswith("loc") and e.text]
            if not locs:
                problems.append(("/sitemap.xml", "the site map lists no address"))
            wrong = [l for l in locs if prod_host and urllib.parse.urlsplit(l).netloc != prod_host]
            if wrong:
                problems.append(("/sitemap.xml", f"{len(wrong)} addresses are not on the production site, e.g. {wrong[0]}"))
        except ET.ParseError:
            problems.append(("/sitemap.xml", "the site map is not valid XML"))

    drift = []
    if args.previous and os.path.exists(args.previous):
        old = json.load(open(args.previous, encoding="utf-8"))
        labels = {"title": "title", "description": "description", "canonical": "canonical address",
                  "h1": "main heading", "lang": "language", "hreflang": "language versions", "jsonld": "structured data"}
        for path, before in old.items():
            now = snapshot.get(path)
            if now is None:
                drift.append((path, "the page is no longer checked or no longer answers"))
                continue
            for k, label in labels.items():
                if before.get(k) and not now.get(k):
                    drift.append((path, f"{label} disappeared (was: {before[k]})"))
                elif before.get(k) != now.get(k) and now.get(k):
                    drift.append((path, f"{label} changed: {before.get(k)} -> {now.get(k)}"))

    if args.snapshot:
        with open(args.snapshot, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=1, ensure_ascii=False)

    lines = [f"### Google and AI search check: {len(pages)} pages, {len(problems)} problem(s), {len(drift)} change(s) since last time"]
    if problems:
        lines += ["", "**Problems**", "", "| Page | Problem |", "|---|---|"] + [f"| `{p}` | {m} |" for p, m in problems]
    if drift:
        lines += ["", "**Changes since the previous check** (fine if intended)", "", "| Page | Change |", "|---|---|"] + [f"| `{p}` | {m} |" for p, m in drift]
    report = "\n".join(lines)
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as s:
            s.write(report + "\n\n")
    if problems and mode == "block":
        print(f"::error::{len(problems)} search-engine problems.")
        sys.exit(1)
    if problems:
        print(f"::warning::{len(problems)} search-engine problems (warning only).")


if __name__ == "__main__":
    main()
