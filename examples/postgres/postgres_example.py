import json_rm
from json_rm.formatters import PostgresFormatter

SCHEMAFILE = "../../resources/schemas/1.2.246.537.6.1506.7000.2022.1.10.json"

schema = json_rm.JSONSchema.from_file(SCHEMAFILE)
pg_formatter = PostgresFormatter("records", "content", extra_cols=['id'])
print(schema.render(pg_formatter))

