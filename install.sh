#!/usr/bin/env bash
# Install the ai-factory skill by downloading its files one by one from
# raw.githubusercontent.com (works in Claude Code cloud sessions too).
#   bash install.sh            -> ./.claude/skills/ai-factory   (this repository)
#   bash install.sh --user     -> ~/.claude/skills/ai-factory   (every project on this machine)
#   REF=v1.0.0 bash install.sh -> a specific release (default: main)
set -euo pipefail
REPO="vincentsider/ai-factory"
REF="${REF:-main}"
BASE="https://raw.githubusercontent.com/$REPO/$REF"
DEST="./.claude/skills/ai-factory"
[ "${1:-}" = "--user" ] && DEST="$HOME/.claude/skills/ai-factory"

if [ -e "$DEST" ] && [ ! -L "$DEST" ]; then
  echo "Updating $DEST"
elif [ -L "$DEST" ]; then
  echo "$DEST is a symlink (a local clone). Update it with git pull instead."; exit 1
fi
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
curl -fsSL "$BASE/install-files.txt" -o "$TMP/files.txt"
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in skills/ai-factory/*) ;; *) echo "Unexpected path in manifest: $f"; exit 1 ;; esac
  rel="${f#skills/ai-factory/}"
  mkdir -p "$TMP/skill/$(dirname "$rel")"
  curl -fsSL "$BASE/$f" -o "$TMP/skill/$rel"
done < "$TMP/files.txt"
chmod +x "$TMP/skill/templates/"*.sh
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
mv "$TMP/skill" "$DEST"
echo "Installed the ai-factory skill ($REF) in $DEST"
echo "Start it in a project with: /ai-factory"
