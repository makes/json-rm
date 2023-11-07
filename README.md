yayson
======

Transpile JSON schemas into other textual representations.

## Usage

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
