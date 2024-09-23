from typing import TypeVar, List


T = TypeVar("T")


class attrData:
    def __init__(self) -> None:
        self.attr = []
    def append(self, attr) -> None:
        self.attr.append(attr)
    def remove(self, attr) -> None:
        self.attr.remove(attr)


class ContextManager:
    def __init__(self, obj: T, attr_data: attrData) -> None:
        self.obj: T = obj
        self.used_attr: attrData = attr_data
            
    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, traceback):
        to_delete = sorted(set(self.obj.__dict__.keys()) - set(self.used_attr.attr))
        
        [setattr(self.obj, key, getattr(self, key)) for key in self.used_attr.attr]
        [delattr(self.obj, key) for key in reversed(to_delete)]


def delete_unused_attr(obj: T) -> ContextManager:
    dest = ContextManager
    attr_data = attrData()

    class ctx:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            
        def fget(self, dest_cls):
            return self.value
        
        def fset(self, dest_cls, new_value):
            self.value = new_value
            attr_data.append(self.key)

        def fdel(self, dest_cls):
            attrData.remove(self.key)
            delattr(self, self.key)
            del self
    
    for key, value in obj.__dict__.items():
        c = ctx(key, value)
        attr = property(c.fget, c.fset, c.fdel, "{key} attr")
        setattr(dest, key, attr)
    
    return dest(obj, attr_data)

