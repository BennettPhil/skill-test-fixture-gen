# API Reference

## Command

```
python3 scripts/run.py [OPTIONS] <schema-file>
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `schema-file` | Yes | Path to a JSON Schema file (.json) |

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--count` | integer | 5 | Number of fixture objects to generate |
| `--seed` | integer | 42 | Random seed for deterministic output |
| `--format` | string | json | Output format: `json` or `jsonl` |
| `--output` | string | - | Write to file instead of stdout |
| `--compact` | flag | false | Output minified JSON (no indentation) |
| `-h, --help` | flag | - | Show help message |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid arguments or missing schema file |
| 2 | Invalid JSON Schema |

## Output

Outputs a JSON array (or JSONL lines) of generated fixture objects that conform to the given schema.

## Supported Schema Features

| Feature | Support |
|---------|---------|
| `type: string` | Generates plausible text based on field name |
| `type: integer` | Generates integers in range (uses min/max if specified) |
| `type: number` | Generates floats in range |
| `type: boolean` | Generates true/false |
| `type: array` | Generates arrays with items matching `items` schema |
| `type: object` | Recursively generates nested objects |
| `type: null` | Generates null |
| `enum` | Picks from enum values |
| `format: email` | Generates email-like strings |
| `format: date` | Generates ISO date strings |
| `format: date-time` | Generates ISO datetime strings |
| `format: uri` | Generates URL-like strings |
| `format: uuid` | Generates UUID-like strings |
| `required` | Always includes required fields |
| Optional fields | Included ~70% of the time (deterministic with seed) |
| `minLength/maxLength` | Respects string length constraints |
| `minimum/maximum` | Respects numeric range constraints |
| `minItems/maxItems` | Respects array length constraints |
