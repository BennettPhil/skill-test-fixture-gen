---
name: test-fixture-gen
description: Generate realistic test fixture data from JSON Schema files with deterministic seeded output.
version: 0.1.0
license: Apache-2.0
---

# Test Fixture Generator

## Purpose

Generates arrays of realistic test objects from a JSON Schema definition. Handles nested objects, arrays, enums, optional fields, and common string formats. Output is deterministic given a seed value.

## Quick Start

```bash
python3 scripts/run.py --count 5 --seed 42 schema.json
```

## Reference Index

- [references/api.md](references/api.md) — Complete CLI flags, exit codes, and supported schema features
- [references/usage-guide.md](references/usage-guide.md) — Step-by-step walkthrough from basic to advanced
- [references/examples.md](references/examples.md) — Copy-paste examples for common schemas

## Implementation

See `scripts/run.py` — a single Python script with no external dependencies.
