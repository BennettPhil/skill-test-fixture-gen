# Examples

## 1. User Profile Schema

**Schema (`user.json`):**

```json
{
  "type": "object",
  "properties": {
    "id": {"type": "string", "format": "uuid"},
    "name": {"type": "string"},
    "email": {"type": "string", "format": "email"},
    "age": {"type": "integer", "minimum": 18, "maximum": 65},
    "active": {"type": "boolean"}
  },
  "required": ["id", "name", "email"]
}
```

**Command:**

```bash
python3 scripts/run.py --count 2 --seed 42 user.json
```

## 2. Product Catalog

**Schema (`product.json`):**

```json
{
  "type": "object",
  "properties": {
    "sku": {"type": "string"},
    "title": {"type": "string"},
    "price": {"type": "number", "minimum": 0.01, "maximum": 9999.99},
    "category": {"type": "string", "enum": ["electronics", "clothing", "books", "food"]},
    "tags": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 5}
  },
  "required": ["sku", "title", "price"]
}
```

**Command:**

```bash
python3 scripts/run.py --count 3 product.json
```

## 3. Error Cases

**Missing schema file:**

```bash
python3 scripts/run.py nonexistent.json
# Error: file not found: nonexistent.json
# Exit code: 1
```

**No arguments:**

```bash
python3 scripts/run.py
# Error: schema file is required.
# Exit code: 1
```

**Invalid JSON:**

```bash
echo "not json" > bad.json
python3 scripts/run.py bad.json
# Error: invalid JSON in bad.json
# Exit code: 2
```
