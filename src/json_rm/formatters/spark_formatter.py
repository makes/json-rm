from ..Attribute import Attribute
from ..Entity import Entity

dtype_map = {
    "string": "StringType"
    , "number": "DecimalType"
    , "integer": "LongType"
    , "boolean": "BooleanType"
    , "array": "ArrayType"
    , "unknown": ""
    , "null": ""
}

class SparkFormatter():
    def __init__(self):
        pass

    def format_schema(self, schema):
        ret = "schema = StructType([\n"
        ret += self.format_entity(schema.root)
        ret += "])\n"
        return ret

    def format_entity(self, entity, array=False):
        ret = ""
        if not entity.is_root:
            ret += '    ' * entity.depth + f"StructField('{entity.name}', StructType([\n"
        if array:
            ret = f"StructField('{entity.name}', ArrayType(StructType([\n"
        for obj in entity.children:
            if type(obj) == Attribute:
                ret += '    ' * (entity.depth + 1) + self.format_attribute(obj)
            elif type(obj) == Entity:
                ret += self.format_entity(obj)
        ret = ''.join(ret.rsplit(',', 1))
        if not entity.is_root:
            closing_parens = "]))" if not array else "])))"
            ret += '    ' * entity.depth + closing_parens + ",\n"
        return ret

    def format_attribute(self, attr):
        dtype = dtype_map[attr.dtype]
        if not dtype:
            print(attr.name)
            raise ValueError()
        ret = f"StructField('{attr.name}', {dtype}(), True),\n"
        if dtype == 'ArrayType':
            if attr.metadata is not None:
                # object array
                ret = self.format_entity(attr.child_entity, array=True)
        return ret
