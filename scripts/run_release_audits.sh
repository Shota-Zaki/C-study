#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
python scripts/build_expanded.py || exit 1
python scripts/audit_csharp_code.py || exit 1
python scripts/audit_expanded.py || exit 1
python scripts/verify_dotnet.py --build
code=$?
if [ "$code" -eq 2 ]; then
  echo "Site checks completed; .NET remains UNVERIFIED."
  exit 2
fi
exit "$code"
