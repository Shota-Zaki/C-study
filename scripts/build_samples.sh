#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if ! command -v dotnet >/dev/null 2>&1; then echo "UNVERIFIED: dotnet SDK is not installed in this environment."; exit 2; fi
fail=0; total=0
while IFS= read -r proj; do total=$((total+1)); echo "==> $proj"; if ! dotnet build "$proj" --nologo; then fail=$((fail+1)); fi; done < <(find "$ROOT/samples" -name '*.csproj' | sort)
echo "projects=$total failed=$fail"
exit "$fail"
