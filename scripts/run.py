#!/usr/bin/env python3
"""Generate realistic test fixture data from JSON Schema files."""

import json
import random
import string
import sys
from pathlib import Path

FIRST_NAMES = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Hank", "Iris", "Jack"]
LAST_NAMES = ["Smith", "Jones", "Brown", "Davis", "Wilson", "Moore", "Taylor", "Clark", "Hall", "Lee"]
DOMAINS = ["example.com", "test.org", "demo.net", "sample.io", "mock.dev"]
WORDS = ["alpha", "beta", "gamma", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet",
         "kilo", "lima", "mike", "nova", "oscar", "papa", "quebec", "romeo", "sierra", "tango"]
LOREM = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed",
         "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua"]


class FixtureGenerator:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def generate(self, schema: dict) -> object:
        schema_type = schema.get("type", "object")
        if "enum" in schema:
            return self.rng.choice(schema["enum"])
        if isinstance(schema_type, list):
            schema_type = self.rng.choice([t for t in schema_type if t != "null"])
        if schema_type == "object":
            return self._gen_object(schema)
        if schema_type == "array":
            return self._gen_array(schema)
        if schema_type == "string":
            return self._gen_string(schema)
        if schema_type == "integer":
            return self._gen_integer(schema)
        if schema_type == "number":
            return self._gen_number(schema)
        if schema_type == "boolean":
            return self.rng.choice([True, False])
        if schema_type == "null":
            return None
        return None

    def _gen_object(self, schema: dict) -> dict:
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        result = {}
        for key, prop_schema in props.items():
            if key in required or self.rng.random() < 0.7:
                result[key] = self.generate(prop_schema)
        return result

    def _gen_array(self, schema: dict) -> list:
        items_schema = schema.get("items", {"type": "string"})
        min_items = schema.get("minItems", 1)
        max_items = schema.get("maxItems", 5)
        count = self.rng.randint(min_items, max_items)
        return [self.generate(items_schema) for _ in range(count)]

    def _gen_string(self, schema: dict) -> str:
        fmt = schema.get("format")
        if fmt == "email":
            name = self.rng.choice(FIRST_NAMES).lower()
            domain = self.rng.choice(DOMAINS)
            return f"{name}@{domain}"
        if fmt == "date":
            year = self.rng.randint(2020, 2026)
            month = self.rng.randint(1, 12)
            day = self.rng.randint(1, 28)
            return f"{year:04d}-{month:02d}-{day:02d}"
        if fmt == "date-time":
            year = self.rng.randint(2020, 2026)
            month = self.rng.randint(1, 12)
            day = self.rng.randint(1, 28)
            hour = self.rng.randint(0, 23)
            minute = self.rng.randint(0, 59)
            return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00Z"
        if fmt == "uri":
            path = self.rng.choice(WORDS)
            domain = self.rng.choice(DOMAINS)
            return f"https://{domain}/{path}"
        if fmt == "uuid":
            parts = [
                ''.join(self.rng.choices("0123456789abcdef", k=8)),
                ''.join(self.rng.choices("0123456789abcdef", k=4)),
                ''.join(self.rng.choices("0123456789abcdef", k=4)),
                ''.join(self.rng.choices("0123456789abcdef", k=4)),
                ''.join(self.rng.choices("0123456789abcdef", k=12)),
            ]
            return "-".join(parts)
        min_len = schema.get("minLength", 3)
        max_len = schema.get("maxLength", 20)
        length = self.rng.randint(min_len, min(max_len, 30))
        words = self.rng.choices(LOREM, k=max(1, length // 5))
        result = " ".join(words)[:length]
        return result if result else self.rng.choice(WORDS)

    def _gen_integer(self, schema: dict) -> int:
        minimum = schema.get("minimum", 0)
        maximum = schema.get("maximum", 1000)
        return self.rng.randint(minimum, maximum)

    def _gen_number(self, schema: dict) -> float:
        minimum = schema.get("minimum", 0.0)
        maximum = schema.get("maximum", 1000.0)
        return round(self.rng.uniform(minimum, maximum), 2)


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Usage: run.py [OPTIONS] <schema-file>")
        print()
        print("Generate realistic test fixture data from a JSON Schema.")
        print()
        print("Options:")
        print("  --count N      Number of fixtures to generate (default: 5)")
        print("  --seed N       Random seed for deterministic output (default: 42)")
        print("  --format FMT   Output format: json or jsonl (default: json)")
        print("  --output PATH  Write to file instead of stdout")
        print("  --compact      Output minified JSON")
        print("  -h, --help     Show this help message")
        sys.exit(0)

    count = 5
    seed = 42
    fmt = "json"
    output_path = None
    compact = False
    schema_file = None

    i = 0
    while i < len(args):
        if args[i] == "--count" and i + 1 < len(args):
            count = int(args[i + 1]); i += 2
        elif args[i] == "--seed" and i + 1 < len(args):
            seed = int(args[i + 1]); i += 2
        elif args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1]; i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_path = args[i + 1]; i += 2
        elif args[i] == "--compact":
            compact = True; i += 1
        else:
            schema_file = args[i]; i += 1

    if not schema_file:
        print("Error: schema file is required.", file=sys.stderr)
        sys.exit(1)

    path = Path(schema_file)
    if not path.exists():
        print(f"Error: file not found: {schema_file}", file=sys.stderr)
        sys.exit(1)

    try:
        schema = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {schema_file}: {e}", file=sys.stderr)
        sys.exit(2)

    gen = FixtureGenerator(seed=seed)
    fixtures = [gen.generate(schema) for _ in range(count)]

    if fmt == "jsonl":
        lines = [json.dumps(f, separators=(",", ":") if compact else None) for f in fixtures]
        result = "\n".join(lines) + "\n"
    else:
        indent = None if compact else 2
        separators = (",", ":") if compact else None
        result = json.dumps(fixtures, indent=indent, separators=separators) + "\n"

    if output_path:
        Path(output_path).write_text(result)
        print(f"Fixtures written to {output_path}", file=sys.stderr)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
