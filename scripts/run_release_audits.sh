#!/usr/bin/env bash
# Exit 2 means a required .NET verification could not be completed, not success.
set -uo pipefail
cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python}"
case "${1:-}" in
  ""|--browser) ;;
  *) echo "Usage: bash scripts/run_release_audits.sh [--browser]" >&2; exit 1 ;;
esac
"$PYTHON" scripts/build_visual.py || exit 1
"$PYTHON" scripts/audit_visual.py || exit 1
if [ "${1:-}" = "--browser" ]; then
  "$PYTHON" scripts/test_visual_browser.py || exit 1
fi
status=0
for verifier in scripts/verify_dotnet.py scripts/verify_visual_samples.py; do
  "$PYTHON" "$verifier" --build
  result=$?
  if [ "$result" -eq 1 ]; then exit 1; fi
  if [ "$result" -ne 0 ]; then status=2; fi
done
if [ "$status" -eq 2 ]; then
  echo "Site checks completed; .NET compilation remains UNVERIFIED."
fi
exit "$status"
