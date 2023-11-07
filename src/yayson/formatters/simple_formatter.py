class SimpleFormatter():
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
        return ret + '\n'

    def format_attribute(self, attr):
        name = '.'.join(attr.name)
        return attr.member_of_entity.depth * '  ' + f"- {name} {'.'.join(attr.path)} {attr.dtype}\n"

