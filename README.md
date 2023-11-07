json-rm
=======

Parse JSON Schemas into relational model and transpile into other textual representations.

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

