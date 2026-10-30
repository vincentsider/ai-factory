#!/usr/bin/env bash
# Every check, the same locally and in CI. Run from the repository root.
set -euo pipefail
S=skills/ai-factory
echo "== hook tests"
bash $S/templates/test-pipeline-guard.sh $S/templates/pipeline-guard.sh
echo "== skill front matter"
python3 tests/validate_skill.py $S
echo "== install manifest matches the skill files"
diff <(find $S -type f | sort) install-files.txt
echo "== no em or en dashes"
python3 - "$S" README.md <<'PY'
import pathlib, sys
bad = []
for root in sys.argv[1:]:
    p = pathlib.Path(root)
    for f in ([p] if p.is_file() else [x for x in p.rglob("*") if x.is_file()]):
        for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            if "\u2013" in line or "\u2014" in line:
                bad.append(f"{f}:{n}")
if bad:
    print("Long dashes found:", *bad, sep="\n  "); sys.exit(1)
print("none")
PY
echo "== workflow templates lint (actionlint, if installed)"
if command -v actionlint >/dev/null; then
  D=$(mktemp -d); mkdir -p "$D/.github/workflows"; cp $S/templates/*.yml "$D/.github/workflows/"; rm "$D/.github/workflows/dependabot.yml"
  (cd "$D" && git init -q && actionlint)
  rm -rf "$D"
fi
echo "== shellcheck (if installed)"
if command -v shellcheck >/dev/null; then shellcheck $S/templates/*.sh install.sh tests/run.sh; fi
echo "All checks passed."
