class Entity:
    def __init__(self, path, metadata, enclosing_attr=None):
        self._path = path
        self._metadata = metadata
        self._enclosing_attr = enclosing_attr # if the contents of the Entity are enclosed within a JSON array attribute
        self._attributes = []
        self._children = []

    def __getitem__(self, index):
        return self._attributes[index]
    
    def __str__(self):
        ret = f"E: {self.name}\n"
        ret += '\n'.join('A: ' + str(a) for a in self._attributes) + '\n'
        return ret

    @property
    def name(self):
        if not self._path:
            return None
        return self._path[-1]

    @property
    def path(self):
        return tuple(self._path)

    @property
    def depth(self):
        return len(self.path)

    @property
    def is_root(self):
        return self.name is None

    @property
    def children(self):
        return tuple(self._children)

    @property
    def metadata(self):
        return self._metadata

    @property
    def enclosing_attr(self):
        return self._enclosing_attr

    def add_attribute(self, attr):
        self.add_child(attr)
        self._attributes.append(attr)

    def add_child(self, obj):
        self._children.append(obj)
