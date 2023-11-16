class SimpleFormatter():
    def __init__(self):
        pass

    def format_schema(self, schema):
        ret = ""
        if schema.title:
            ret += f"Title: {schema.title}\n"
        if schema.description:
            ret += f"Description: {schema.description}\n"
        for e in schema:
            ret += self.format_entity(e)
        return ret

    def format_entity(self, entity):
        name = '.'.join(entity.path)
        ret = entity.depth * '  ' + f"{name}\n"
        for a in entity:
            ret += self.format_attribute(a)
        return ret + '\n'

    def format_attribute(self, attr):
        name = '.'.join(attr.subpath)
        return attr.member_of_entity.depth * '  ' + f"- {name} {'.'.join(attr.path)} {attr.dtype}\n"

