import json
import jsonref

from .Attribute import Attribute
from .Entity import Entity

class JSONSchema:
    def __init__(self, schema, normalization=False):
        self._title = ""
        self._description = ""
        self._schema = jsonref.loads(schema)
        self._normalization = normalization

        self._metadata = {key:self._schema[key] for key in self._schema if key != 'properties'}
        if "title" in self._metadata:
            self._title = self._metadata["title"]
        if "description" in self._metadata:
            self._description = self._metadata["description"]

        self._entities = []
        self._recurse(self._schema["properties"])

    @classmethod
    def from_file(cls, path, normalization=False, encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as f:
            schema = f.read()
        return cls(schema, normalization)

    def __getitem__(self, index):
        return self._entities[index]

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def root(self):
        if not self._entities:
            return None
        return self._entities[0]

    @property
    def normalization(self):
        return self._normalization

    def render(self, formatter):
        return formatter.format_schema(self)

    #def render_entities(self, formatter, ignore_empty=False):
    #    ret = ""
    #    for e in self._entities:
    #        ret += e.render(formatter, ignore_empty)
    #    return ret

    def _infer_datatype(self, prop):
        if any(item in prop for item in ["anyOf", "allOf", "oneOf", "not"]):
            return 'unknown' # nested schemas are not supported

        if "type" not in prop:
            return 'string'

        if type(prop["type"]) == str:
            return prop["type"] # single type specified

        # if multiple types are given, infer:
        if type(prop["type"]) == list:
            types = set(t for t in prop["type"] if t != 'null')
            if len(types) == 0:
                return 'null'
            if len(types) == 1:
                return list(types)[0]
            if 'object' in types:
                return 'unknown'
            return 'string'
        else:
            raise ValueError("Unable to parse 'type'.")

    def _extract_metadata(self, prop):
        return {key:prop[key] for key in prop if key not in ['properties', 'items']}

    def _recurse(self, json_obj, path=[], entity=None, name_level=1, path_level=0):
        if not entity and not self._entities:
            # create root entity
            entity = Entity(path, None)
        #if entity and entity not in self._entities:
        if entity not in self._entities:
            self._entities.append(entity)
        if type(json_obj) == dict:
            for name, prop in json_obj.items():
                datatype = self._infer_datatype(prop)
                metadata = self._extract_metadata(prop)
                if datatype == "object":
                    #if not entity and not self._entities:
                    #    entity = Entity([name], path_level, metadata)
                    if not self._normalization:
                        self._recurse(prop["properties"], path=path+[name], entity=entity, name_level=name_level, path_level=path_level)
                    else:
                        assert(entity)
                        e = Entity(path+[name], metadata)
                        entity.add_child(e)
                        self._recurse(prop["properties"], path=path+[name], entity=e, name_level=name_level+1, path_level=path_level)
                elif datatype == "array":
                    assert(entity)
                    attrname = path[name_level:]+[name]
                    path_skip = path_level + 1 if path_level > 0 else 0
                    array = Attribute(attrname, path[path_skip:]+[name], datatype, entity, metadata)
                    items_metadata = {key:prop["items"][key] for key in prop["items"] if key != 'properties'}
                    array_entity = Entity(path+[name], items_metadata, enclosing_attr=array)
                    #entity.add_child(array_entity)
                    array.child_entity = array_entity
                    entity.add_attribute(array)
                    if "properties" not in prop["items"]:
                        # handle scalar array
                        dtype = self._infer_datatype(prop["items"])
                        # use metadata=None to detect scalar array (metadata is in `array_entity`).
                        array_entity.add_attribute(Attribute(path[len(path)+1:]+[name], path[len(path)+1:]+[name], dtype, array_entity, None))
                        self._entities.append(array_entity)
                    else:
                        self._recurse(prop["items"]["properties"], path=path+[name], entity=array_entity, name_level=len(path)+1, path_level=len(path))
                else:
                    attrname = path[name_level:]+[name]
                    path_skip = path_level + 1 if path_level > 0 else 0
                    entity.add_attribute(Attribute(attrname, path[path_skip:]+[name], datatype, entity, metadata))

