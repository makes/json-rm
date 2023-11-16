PG_MAX_IDENTIFIER_LENGTH = 63

typecast_map = {
    "string": "::text"
    , "number": "::numeric"
    , "integer": "::integer"
    , "boolean": "::bool"
    , "array": "::jsonb"
    , "unknown": "::jsonb"
    , "null": ""
}

class PostgresFormatter():
    db_object_types = {'view': 'VIEW', 'mview': 'MATERIALIZED VIEW', 'table': 'TABLE'}

    def __init__(self, table, column,
                 obj_type='view',
                 pg_schema=None,
                 root_relation_name='root',
                 ignore_empty=False,
                 drop=False,
                 extra_cols=[]):
        self._table = table
        self._column = column
        self._obj_type = obj_type
        self._pg_schema = pg_schema
        self._root_relation_name = root_relation_name
        self._ignore_empty = ignore_empty
        self._drop = drop
        self._extra_cols = extra_cols

    def _format_name(self, name):
        name_str = '.'.join(name)
        if not name:
            name_str = self._root_relation_name
        return self._truncate_identifier(name_str)

    def _truncate_identifier(self, identifier):
        while len(identifier) > PG_MAX_IDENTIFIER_LENGTH:
            if '.' not in identifier:
                break
            identifier = identifier.split('.', 1)[1]
        return identifier

    def format_schema(self, schema):
        ret = ""
        for e in schema:
            if self._ignore_empty and len(e) == 0:
                continue
            ret += self.format_entity(e)
        return ret

    def format_entity(self, entity):
        schema = ""
        if self._pg_schema:
            schema = f'"{self._pg_schema}".'
        enclosing_attr = entity.enclosing_attr
        ret = ""
        name = self._format_name(entity.path)
        _type = PostgresFormatter.db_object_types[self._obj_type]
        if self._drop:
            ret += f'DROP {_type} IF EXISTS {schema}"{name}" CASCADE;\n'
        ret += f'CREATE {_type} {schema}"{name}" AS SELECT\n'
        prefix = ' '
        for col in self._extra_cols:
            ret += 4 * ' ' + col + '\n'
            prefix = ', '
        for col in entity:
            ret += 4 * ' ' + prefix + self.format_attribute(col) + '\n'
            prefix = ', '
        if not enclosing_attr:
            ret += f'FROM {schema}"{self._table}";'
        else:
            src_tbl_name = self._format_name(enclosing_attr.member_of_entity.path)
            src_col_name = self._format_name(enclosing_attr.subpath)
            ret += f'FROM {schema}"{src_tbl_name}" src_tbl, jsonb_array_elements(src_tbl."{src_col_name}") arr ("{src_col_name}");'
        return ret + '\n\n'

    def format_attribute(self, attr):
        typecast = typecast_map[attr.dtype]
        quoted_path = [f"'{x}'" for x in attr.path]
        col_name = self._format_name(attr.subpath)
        src_attr = attr.member_of_entity.enclosing_attr
        if not src_attr:
            ret = f"({'->'.join([self._column]+quoted_path)}){typecast} AS \"{col_name}\""
        else:
            src_col_name = '"' + self._format_name(src_attr.subpath) + '"'
            if attr.metadata is not None:
                # object array (key-value pairs)
                ret = f"(arr.{'->'.join([src_col_name]+quoted_path)}){typecast} AS \"{col_name}\""
            else:
                # scalar array
                ret = f"arr.{src_col_name}{typecast} AS \"{col_name}\""
        if typecast != "::jsonb":
            ret = '->>'.join(ret.rsplit('->', 1)) # replace rightmost arrow with ->> to cast to string and allow JSON nulls to be converted to SQL nulls
        return ret
