#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python scripts/validate_static.py
python scripts/link_audit.py
python scripts/http_smoke.py
python scripts/a11y_audit.py
python scripts/audit_csharp_code.py
python scripts/browser_audit.py

set +e
./scripts/build_samples.sh
sdk_rc=$?
set -e
if [ "$sdk_rc" -eq 2 ]; then
  echo "C# compiler validation: UNVERIFIED (SDK unavailable in this environment)."
  exit 0
fi
exit "$sdk_rc"
