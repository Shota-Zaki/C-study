#!/usr/bin/env bash
# Compatibility entry point; preserves UNVERIFIED exit code 2.
exec bash "$(dirname "$0")/run_release_audits.sh" "$@"
