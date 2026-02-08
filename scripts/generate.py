#!/usr/bin/env python3
"""Test fixture generator - creates realistic sample data from JSON schemas."""

import json, sys, random, argparse, string
from datetime import datetime, timedelta

FIRST_NAMES = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Iris', 'Jack']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Moore']
DOMAINS = ['example.com', 'test.org', 'demo.net']
WORDS = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'theta', 'iota', 'kappa', 'lambda']


def generate_value(schema, prop_name=''):
    schema_type = schema.get('type', 'string')
    name_lower = prop_name.lower()

    if 'enum' in schema:
        return random.choice(schema['enum'])

    if 'const' in schema:
        return schema['const']

    if schema_type == 'string':
        fmt = schema.get('format', '')
        if fmt == 'email' or 'email' in name_lower:
            return f'{random.choice(FIRST_NAMES).lower()}@{random.choice(DOMAINS)}'
        if fmt == 'date-time' or name_lower.endswith(('_at', '_date', 'timestamp')):
            base = datetime(2024, 1, 1)
            delta = timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
            return (base + delta).isoformat() + 'Z'
        if fmt == 'date':
            return f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
        if fmt == 'uri' or 'url' in name_lower:
            return f'https://{random.choice(DOMAINS)}/{random.choice(WORDS)}'
        if fmt == 'uuid' or 'id' in name_lower:
            return f'{random.randint(10000,99999):05d}-{random.randint(1000,9999)}'
        if 'name' in name_lower:
            return f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}'
        if 'phone' in name_lower:
            return f'+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}'
        if 'description' in name_lower or 'bio' in name_lower:
            return ' '.join(random.choices(WORDS, k=random.randint(5, 10)))

        min_len = schema.get('minLength', 3)
        max_len = schema.get('maxLength', 20)
        length = random.randint(min_len, min(max_len, 20))
        return ' '.join(random.choices(WORDS, k=max(1, length // 6)))

    if schema_type == 'integer':
        minimum = schema.get('minimum', 1)
        maximum = schema.get('maximum', 1000)
        return random.randint(int(minimum), int(maximum))

    if schema_type == 'number':
        minimum = schema.get('minimum', 0.0)
        maximum = schema.get('maximum', 1000.0)
        return round(random.uniform(float(minimum), float(maximum)), 2)

    if schema_type == 'boolean':
        return random.choice([True, False])

    if schema_type == 'array':
        items_schema = schema.get('items', {'type': 'string'})
        min_items = schema.get('minItems', 1)
        max_items = schema.get('maxItems', 5)
        count = random.randint(min_items, max_items)
        return [generate_value(items_schema) for _ in range(count)]

    if schema_type == 'object':
        obj = {}
        props = schema.get('properties', {})
        for key, prop_schema in props.items():
            obj[key] = generate_value(prop_schema, key)
        return obj

    if schema_type == 'null':
        return None

    return ' '.join(random.choices(WORDS, k=2))


def main():
    parser = argparse.ArgumentParser(description='Generate test fixtures from JSON schema')
    parser.add_argument('input_file', nargs='?', help='JSON schema file (reads stdin if omitted)')
    parser.add_argument('--count', type=int, default=1, help='Number of fixtures (default: 1)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    parser.add_argument('--compact', action='store_true', help='Compact JSON output')
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.input_file:
        with open(args.input_file) as f:
            schema = json.load(f)
    else:
        input_data = sys.stdin.read()
        if not input_data.strip():
            print('Error: No input provided', file=sys.stderr)
            sys.exit(1)
        try:
            schema = json.loads(input_data)
        except json.JSONDecodeError as e:
            print(f'Error: Invalid JSON schema: {e}', file=sys.stderr)
            sys.exit(1)

    if args.count == 1:
        result = generate_value(schema)
    else:
        result = [generate_value(schema) for _ in range(args.count)]

    if args.compact:
        print(json.dumps(result, separators=(',', ':')))
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
