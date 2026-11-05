#!/usr/bin/env python3
"""Install the third-party skills listed in vendor-lock.json into a project.

Each file is downloaded from raw.githubusercontent.com at the exact commit in
the lock file and checked against its sha256. One wrong file and nothing is
installed for that entry. A SOURCE.md with the author, licence, commit and
date is written next to the files (the licences require attribution).

Usage, from the project root:
  python3 fetch-vendored.py path/to/vendor-lock.json [entry-name ...]
With no names, every entry is installed. Exit code 1 on any failure.
Works in Claude Code cloud sessions (raw.githubusercontent.com is reachable).
"""
import datetime
import hashlib
import json
import os
import pathlib
import shutil
import sys
import tempfile
import urllib.request

BASE = os.environ.get("VENDOR_BASE_URL", "https://raw.githubusercontent.com")


def install(entry, root):
    dest = (root / entry["dest"]).resolve()
    if root.resolve() not in dest.parents:
        raise SystemExit(f"{entry['name']}: destination {entry['dest']} is outside the project")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for f in entry["files"]:
            rel = pathlib.PurePosixPath(f["dest"])
            if rel.is_absolute() or ".." in rel.parts:
                raise SystemExit(f"{entry['name']}: unsafe path {f['dest']}")
            url = f"{BASE}/{entry['repo']}/{entry['commit']}/{f['src']}"
            with urllib.request.urlopen(url, timeout=30) as r:
                data = r.read()
            got = hashlib.sha256(data).hexdigest()
            if got != f["sha256"]:
                raise SystemExit(f"{entry['name']}: {f['src']} does not match the lock file (got {got[:12]}, want {f['sha256'][:12]}). Nothing installed.")
            out = tmp / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        (tmp / "SOURCE.md").write_text(
            f"# Source of these files\n\n"
            f"- Project: https://github.com/{entry['repo']}\n"
            f"- Commit: {entry['commit']}\n"
            f"- Author: {entry['author']}\n"
            f"- Licence: {entry['license']}\n"
            f"- Installed by the ai-factory skill on {datetime.date.today().isoformat()}, unchanged, each file checked against its sha256.\n"
        )
        dest.mkdir(parents=True, exist_ok=True)
        for item in tmp.iterdir():
            target = dest / item.name
            if target.is_dir():
                shutil.rmtree(target)
            shutil.move(str(item), str(target))
    print(f"Installed {entry['name']} ({len(entry['files'])} files, commit {entry['commit'][:7]}) in {entry['dest']}")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    lock = json.loads(pathlib.Path(sys.argv[1]).read_text())
    wanted = set(sys.argv[2:])
    entries = [e for e in lock["entries"] if not wanted or e["name"] in wanted]
    missing = wanted - {e["name"] for e in entries}
    if missing:
        raise SystemExit(f"Unknown entries: {', '.join(sorted(missing))}")
    for e in entries:
        install(e, pathlib.Path.cwd())


if __name__ == "__main__":
    main()
