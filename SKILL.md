---
name: test-fixture-gen
description: Generates realistic test fixtures from JSON Schema definitions with smart field detection.
version: 0.1.0
license: Apache-2.0
---

# Test Fixture Generator

## Purpose

Generate realistic sample data for testing from JSON Schema definitions. Understands property names (email, name, phone, url) and schema formats to produce contextually appropriate values instead of random gibberish.

## Quick Start

```bash
$ echo '{"type":"object","properties":{"name":{"type":"string"},"age":{"type":"integer"}}}' | ./scripts/run.sh
{
  "name": "Alice Smith",
  "age": 42
}
```

## Usage Examples

### Multiple Fixtures

```bash
$ echo '{"type":"object","properties":{"id":{"type":"integer"},"email":{"type":"string","format":"email"}}}' | ./scripts/run.sh --count 3
```

### Reproducible Output

```bash
$ echo '{"type":"object","properties":{"x":{"type":"integer"}}}' | ./scripts/run.sh --seed 42
```

### Array Schema

```bash
$ echo '{"type":"array","items":{"type":"string"},"minItems":3}' | ./scripts/run.sh
```

### From File

```bash
$ ./scripts/run.sh schema.json --count 10 --seed 123
```

## Options Reference

| Flag        | Default | Description                          |
|-------------|---------|--------------------------------------|
| `--count N` | 1       | Number of fixtures to generate       |
| `--seed N`  | random  | Random seed for reproducibility      |
| `--compact` | false   | Compact JSON output                  |
| `--help`    |         | Show usage                           |

## Error Handling

| Exit Code | Meaning            |
|-----------|--------------------|
| 0         | Success            |
| 1         | Usage/input error  |

## Validation

Run `scripts/test.sh` to verify correctness (7 assertions).
