#!/usr/bin/env python3
"""Check that every old address of a website still leads to the right page.

Reads a CSV file with two columns, old address then new address (a header
line "old,new" is allowed). For each line, against BASE_URL:
  1. the old address answers a permanent redirect (301 or 308),
  2. the redirect points to the new address, in one step (no chain),
  3. the new address answers 200.
Addresses may be paths (/restaurants/le-mas) or full URLs; full URLs are
checked on BASE_URL's host, so the same file works for staging and production.

Usage: python3 check-redirects.py redirects.csv https://staging.example.com
Mode: REDIRECTS_MODE=block (default) exits 1 on any failure; =warn only reports.
Access to a protected staging site: CF_ACCESS_CLIENT_ID and
CF_ACCESS_CLIENT_SECRET (Cloudflare Access service token), or EXTRA_HEADER
("Name: value"). A table is added to $GITHUB_STEP_SUMMARY when it is set.
"""
import csv
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


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


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url):
    req = urllib.request.Request(url, headers=headers(), method="GET")
    try:
        with OPENER.open(req, timeout=20) as r:
            return r.status, r.headers.get("Location")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, str(e)


def on_base(address, base):
    p = urllib.parse.urlsplit(address)
    b = urllib.parse.urlsplit(base)
    path = p.path or "/"
    return urllib.parse.urlunsplit((b.scheme, b.netloc, path, p.query, ""))


def same_target(location, expected, base):
    if not location:
        return False
    loc = urllib.parse.urlsplit(urllib.parse.urljoin(base, location))
    exp = urllib.parse.urlsplit(on_base(expected, base))
    norm = lambda s: (s.path.rstrip("/") or "/", s.query)
    return norm(loc) == norm(exp)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    csv_path, base = sys.argv[1], sys.argv[2].rstrip("/")
    mode = os.environ.get("REDIRECTS_MODE", "block")
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0].strip().startswith("#") or row[0].strip().lower() == "old":
                continue
            if len(row) < 2:
                rows.append((row[0].strip(), "", "the line has no new address"))
                continue
            rows.append((row[0].strip(), row[1].strip(), None))
    failures = []
    for old, new, problem in rows:
        if problem is None:
            status, location = fetch(on_base(old, base))
            if status not in (301, 308):
                problem = f"answers {status}, not a permanent redirect" if status else f"cannot be reached ({location})"
            elif not same_target(location, new, base):
                problem = f"redirects to {location}, expected {new}"
            else:
                s2, _ = fetch(on_base(new, base))
                if s2 != 200:
                    problem = f"the new page answers {s2}" + (" (a redirect chain)" if s2 in (301, 302, 307, 308) else "")
        if problem:
            failures.append((old, new, problem))
    ok = len(rows) - len(failures)
    lines = [f"### Old addresses: {ok} of {len(rows)} lead to the right page"]
    if failures:
        lines += ["", "| Old address | Expected | Problem |", "|---|---|---|"]
        lines += [f"| `{o}` | `{n}` | {p} |" for o, n, p in failures[:200]]
        if len(failures) > 200:
            lines.append(f"\n...and {len(failures) - 200} more.")
    report = "\n".join(lines)
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as s:
            s.write(report + "\n\n")
    if failures and mode == "block":
        print(f"::error::{len(failures)} old addresses do not lead to the right page.")
        sys.exit(1)
    if failures:
        print(f"::warning::{len(failures)} old addresses do not lead to the right page (warning only).")


if __name__ == "__main__":
    main()
