import typer
from typing import Optional
from typing_extensions import Annotated

from .JSONSchema import JSONSchema
from . import formatters

main = typer.Typer()

@main.command()
def postgres(input: str):
    schema = JSONSchema.from_file(input)
    pg_formatter = formatters.PostgresFormatter("records", "content", extra_cols=['id'])
    print(schema.render(pg_formatter))

@main.command()
def simple(input: str):
    schema = JSONSchema.from_file(input)
    simple_formatter = formatters.SimpleFormatter()
    print(schema.render(simple_formatter))

if __name__ == "__main__":
    main()
