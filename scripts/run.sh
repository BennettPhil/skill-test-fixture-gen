#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${1:-}" = "--help" ]]; then
  cat <<'EOF' >&2
Usage: run.sh [INPUT_FILE] [OPTIONS]

Generates test fixtures from JSON schema. Reads from stdin if no file.

Options:
  --count N    Number of fixtures to generate (default: 1)
  --seed N     Random seed for reproducible output
  --compact    Compact JSON output
  --help       Show this help message
EOF
  exit 0
fi

exec python3 "$SCRIPT_DIR/generate.py" "$@"
