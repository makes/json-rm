class Entity:
    def __init__(self, name, depth, metadata, enclosing_attr=None):
        self._name = name
        self._depth = depth
        self._metadata = metadata
        self._enclosing_attr = enclosing_attr # if the contents of the Entity are enclosed within a JSON array attribute
        self._attributes = []

    def __getitem__(self, index):
        return self._attributes[index]

    def render(self, formatter, ignore_empty=False):
        if ignore_empty and len(self._attributes) == 0:
            return ""
        return formatter.format_entity(self)

    @property
    def name(self):
        return self._name

    @property
    def depth(self):
        return self._depth

    @property
    def metadata(self):
        return self._metadata

    @property
    def enclosing_attr(self):
        return self._enclosing_attr

    def add_attribute(self, attr):
        self._attributes.append(attr)

