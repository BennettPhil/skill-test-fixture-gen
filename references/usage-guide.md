# Usage Guide

## Basic Usage

Given a JSON Schema file, generate test fixtures:

```bash
python3 scripts/run.py schema.json
```

This produces 5 fixture objects (default) using seed 42.

## Controlling Output Count

```bash
python3 scripts/run.py --count 10 schema.json
```

## Deterministic Output

The same seed always produces the same output:

```bash
python3 scripts/run.py --seed 123 schema.json
# Running again with --seed 123 produces identical output
```

Different seeds produce different data:

```bash
python3 scripts/run.py --seed 1 schema.json   # dataset A
python3 scripts/run.py --seed 2 schema.json   # dataset B
```

## Output Formats

### JSON Array (default)

```bash
python3 scripts/run.py schema.json
# [{"name": "Alice", "age": 34}, ...]
```

### JSON Lines

```bash
python3 scripts/run.py --format jsonl schema.json
# {"name": "Alice", "age": 34}
# {"name": "Bob", "age": 28}
```

### Compact JSON

```bash
python3 scripts/run.py --compact schema.json
# [{"name":"Alice","age":34},...]
```

## Writing to File

```bash
python3 scripts/run.py --output fixtures.json schema.json
```

## Schema Examples

### Simple Object

```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer", "minimum": 18, "maximum": 99}
  },
  "required": ["name", "age"]
}
```

### Nested Objects with Arrays

```json
{
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "email": {"type": "string", "format": "email"},
        "tags": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 3}
      }
    }
  }
}
```

### Enums

```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["active", "inactive", "pending"]}
  }
}
```
