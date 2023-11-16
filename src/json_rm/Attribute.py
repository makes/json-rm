class Attribute:
    def __init__(self, subpath, path, dtype, member_of_entity, metadata):
        self._subpath = subpath
        self._path = path
        self._dtype = dtype
        self._member_of_entity = member_of_entity
        self._metadata = metadata
        self._child_entity = None

    def __str__(self):
        return f'{self._dtype} {self.name}'

    @property
    def name(self):
        return self._subpath[-1]

    @property
    def subpath(self):
        return tuple(self._subpath)

    @property
    def path(self):
        return tuple(self._path)

    @property
    def dtype(self):
        return self._dtype

    @property
    def member_of_entity(self):
        return self._member_of_entity

    @property
    def metadata(self):
        return self._metadata

    @property
    def child_entity(self):
        return self._child_entity

    @child_entity.setter
    def child_entity(self, entity):
        self._child_entity = entity

    #def render(self, formatter):
    #    return formatter.format_attribute(self)

