#!/usr/bin/env bash
# verify-live.sh BASE_URL EXPECTED_SHA [PATH ...]
# Waits until BASE_URL + $VERSION_PATH (default /version.json) reports the
# expected commit in its "version" field (first 7 characters compared), then
# checks that every PATH answers HTTP 200. Used by deploy-staging,
# promote-production and rollback. Exit 1 with a clear message otherwise.
set -euo pipefail
BASE="${1:?base url}"; WANT="${2:?expected sha}"; shift 2
WANT="${WANT:0:7}"
VP="${VERSION_PATH:-/version.json}"
TRIES="${VERIFY_TRIES:-60}"
for i in $(seq 1 "$TRIES"); do
  GOT=$(curl -fsS --max-time 10 "$BASE$VP" 2>/dev/null \
    | python3 -c 'import json,sys
try:
  d=json.load(sys.stdin); print(str(d.get("version") or d.get("commit") or d.get("sha") or "")[:7])
except Exception: print("")' || true)
  if [ "$GOT" = "$WANT" ]; then echo "Live on $WANT ($BASE)"; break; fi
  echo "Live version '${GOT:-none}', waiting for '$WANT' ($i/$TRIES)"; sleep 10
  [ "$i" = "$TRIES" ] && { echo "::error::$BASE never reported commit $WANT"; exit 1; }
done
fail=0
for p in "$@"; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$BASE$p")
  echo "$p -> $code"; [ "$code" = "200" ] || fail=1
done
[ "$fail" = 0 ] || { echo "::error::A key page did not answer 200"; exit 1; }
