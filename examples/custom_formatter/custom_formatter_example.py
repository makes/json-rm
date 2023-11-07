import json_rm

SCHEMAFILE = "../../resources/schemas/1.2.246.537.6.1506.7000.2022.1.10.json"

schema = json_rm.JSONSchema.from_file(SCHEMAFILE, normalization=True)

class CustomFormatter():
    def __init__(self):
        pass

    def format_schema(self, schema, ignore_empty):
        ret = ""
        if schema.title:
            ret += f"Title: {schema.title}\n"
        if schema.description:
            ret += f"Description: {schema.description}\n"
        ret += schema.render_entities(self, ignore_empty)
        return ret

    def format_entity(self, entity):
        name = '.'.join(entity.name)
        ret = entity.depth * '  ' + f"{name}\n"
        for a in entity:
            ret += a.render(self)
        return ret

    def format_attribute(self, attr):
        name = '.'.join(attr.name)
        return attr.member_of_entity.depth * '  ' + f"- {name} {'.'.join(attr.path)} {attr.dtype}\n"


print(schema.render(CustomFormatter()))
