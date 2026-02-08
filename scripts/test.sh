#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN="$SCRIPT_DIR/run.sh"
PASS=0; FAIL=0; TOTAL=0

assert_contains() {
  local desc="$1" needle="$2" haystack="$3"
  ((TOTAL++))
  if echo "$haystack" | grep -qF -- "$needle"; then
    ((PASS++)); echo "  PASS: $desc"
  else
    ((FAIL++)); echo "  FAIL: $desc (output missing '$needle')"
  fi
}

assert_exit_code() {
  local desc="$1" expected="$2"
  shift 2
  local output
  set +e; output=$("$@" 2>&1); local actual=$?; set -e
  ((TOTAL++))
  if [ "$expected" -eq "$actual" ]; then
    ((PASS++)); echo "  PASS: $desc"
  else
    ((FAIL++)); echo "  FAIL: $desc (expected exit $expected, got $actual)"
  fi
}

echo "=== Tests for test-fixture-gen ==="

echo "Core:"
# Basic JSON schema input
result=$(echo '{"type":"object","properties":{"name":{"type":"string"},"age":{"type":"integer"}}}' | "$RUN")
assert_contains "generates name field" '"name"' "$result"
assert_contains "generates age field" '"age"' "$result"

# Array type
result=$(echo '{"type":"array","items":{"type":"string"}}' | "$RUN")
assert_contains "generates array" "[" "$result"

# Count flag
result=$(echo '{"type":"object","properties":{"id":{"type":"integer"}}}' | "$RUN" --count 3)
assert_contains "count flag generates array" "[" "$result"

echo "Input validation:"
assert_exit_code "empty stdin errors" 1 "$RUN" < /dev/null

echo "Help:"
result=$("$RUN" --help 2>&1)
assert_contains "help flag works" "Usage:" "$result"

echo "Seed:"
result1=$(echo '{"type":"object","properties":{"x":{"type":"integer"}}}' | "$RUN" --seed 42)
result2=$(echo '{"type":"object","properties":{"x":{"type":"integer"}}}' | "$RUN" --seed 42)
((TOTAL++))
if [ "$result1" = "$result2" ]; then
  ((PASS++)); echo "  PASS: seed produces reproducible output"
else
  ((FAIL++)); echo "  FAIL: seed produces different output"
fi

echo ""
echo "=== Results: $PASS/$TOTAL passed ==="
[ "$FAIL" -eq 0 ] || { echo "BLOCKED: $FAIL test(s) failed"; exit 1; }
