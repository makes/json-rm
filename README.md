json-rm
=======

This tool parses a JSON Schema into "Entities" and "Attributes", which correspond to tables and columns in a relational database. It can be used to output different representations of the data model described by the input schema.

## Installation

```
pip install json-rm
```

## Command line usage

```
jst <command> <schema_path>
```

### Examples

Use the 'simple' formatter on a schema:

```
$ jst simple resources/schemas/1.2.246.537.6.1506.7000.2022.1.10.json
```

Use the 'postgres' formatter on a schema:

```
$ jst postgres resources/schemas/1.2.246.537.6.1506.7000.2022.1.10.json
```

## Using from your Python code

```
import json_rm
from json_rm.formatters import SimpleFormatter

schema = json_rm.JSONSchema.from_file("schema.json")
formatter = SimpleFormatter()

print(schema.render(formatter))
```

## Parsing options

### normalization

- Denormalized (default) mode results in a flat structure with less tables.
- Normalized mode results in a deep structure with more tables.

When `normalization` is set to `False` (default), the parser operates in "denormalized" mode, creating a new `Entity` only for the root object and repeating (`array`) objects. In the "normalized mode, a separate `Entity` is created for each nested structure (JSON objects and arrays).
