#!/usr/bin/env python3
"""Make sure the share of code covered by tests does not go down.

Reads the coverage report the test tool wrote, compares it with the share
measured on main, and reports. On main it only records the new reference.

Understood formats (detected from the file):
  coverage-summary.json   Vitest, Jest, c8 (json-summary reporter): total.lines.pct
  coverage.json           Python coverage.py (`coverage json`): totals.percent_covered
  lcov.info               any lcov reporter: sum of LH / sum of LF
  coverage.xml            Cobertura (pytest-cov --cov-report=xml, others): line-rate
  cover.txt               Go `go tool cover -func=cover.out > cover.txt`: "total:" line

Usage: python3 coverage-check.py REPORT [--baseline FILE] [--write FILE]
  --baseline  a file holding the reference share (a number), from main
  --write     where to write the share measured now (to keep as the next reference)
Env: COVERAGE_MODE=warn (default) or block; COVERAGE_TOLERANCE (default 0.2 points).
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET


def read_pct(path):
    name = os.path.basename(path)
    text = open(path, encoding="utf-8").read()
    if name.endswith(".info"):
        lh = sum(int(x) for x in re.findall(r"^LH:(\d+)", text, re.M))
        lf = sum(int(x) for x in re.findall(r"^LF:(\d+)", text, re.M))
        return 100.0 * lh / lf if lf else 0.0
    if name.endswith(".xml"):
        return 100.0 * float(ET.fromstring(text).get("line-rate", "0"))
    if name.endswith(".json"):
        d = json.loads(text)
        if "total" in d:
            return float(d["total"]["lines"]["pct"])
        if "totals" in d:
            return float(d["totals"]["percent_covered"])
        raise SystemExit(f"{path}: unknown JSON coverage format")
    m = re.search(r"^total:\s+\(statements\)\s+([\d.]+)%", text, re.M)
    if m:
        return float(m.group(1))
    raise SystemExit(f"{path}: unknown coverage format")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--baseline")
    ap.add_argument("--write")
    a = ap.parse_args()
    mode = os.environ.get("COVERAGE_MODE", "warn")
    tol = float(os.environ.get("COVERAGE_TOLERANCE", "0.2"))
    now = round(read_pct(a.report), 2)
    if a.write:
        with open(a.write, "w") as f:
            f.write(f"{now}\n")
    base = None
    if a.baseline and os.path.exists(a.baseline):
        try:
            base = float(open(a.baseline).read().strip())
        except ValueError:
            base = None
    if base is None:
        msg = f"### Test coverage: {now}% of lines (no reference from main yet)"
        status = "ok"
    elif now + tol < base:
        msg = f"### Test coverage went down: {now}% now, {base}% on main\nAdd tests for the code this change adds or modifies."
        status = "down"
    else:
        msg = f"### Test coverage: {now}% (main: {base}%)"
        status = "ok"
    print(msg)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as s:
            s.write(msg + "\n\n")
    if status == "down":
        if mode == "block":
            print("::error::Test coverage went down.")
            sys.exit(1)
        print("::warning::Test coverage went down (warning only).")


if __name__ == "__main__":
    main()
