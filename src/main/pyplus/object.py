from copy import copy as _copy, deepcopy as _deepcopy

from .table import list2table as _list2table, table2list as _table2list
from .common import isiterable as _isiterable, ispathlike as _ispathlike
from .string import camel_case as _camel_case, snake_case as _snake_case


class LazyObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __copy__(self):
        return type(self)(**self.__dict__)

    def __deepcopy__(self, memo):
        kwargs = {key: _deepcopy(value) for key, value in self.__dict__.items()}
        return type(self)(**kwargs)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.__dict__ == other
        else:
            try:
                return self.__dict__ == other.__dict__
            except AttributeError:
                return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        params = ["%s=%s" % (key, repr(value)) for key, value in self.__dict__.items()]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(params))

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, key))

    def copy(self):
        return _copy(self)

    def deepcopy(self):
        return _deepcopy(self)


class AssignableLazyObject(LazyObject):
    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)


class ImmutableLazyObject(LazyObject):
    def __setattr__(self, key, value):
        raise AttributeError("can't set attribute '%s', '%s' instances are immutable" % (key, type(self).__name__))


# noinspection PyCallByClass
class LazyObjects:
    __CLASS__ = LazyObject

    def __init__(self, iterable=None):
        self.__objects = []

        if _isiterable(iterable):
            self.push(*iterable)

        elif iterable is not None:
            raise TypeError("'%s' object is not iterable" % type(iterable).__name__)

    def __contains__(self, item):
        return any(item is obj for obj in self.__objects)

    def __eq__(self, other):
        if _isiterable(other):
            return self.__objects == list(other)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        return self.__objects[index]

    def __iter__(self):
        return iter(self.__objects)

    def __len__(self):
        return len(self.__objects)

    def __repr__(self):
        return list.__repr__(self.__objects)

    @classmethod
    def from_table(cls, path, parse=True, delimiter=","):
        if _ispathlike(path):
            list_ = _table2list(path, parse=parse, delimiter=delimiter)
            headers = {key: _snake_case(key) for key in list_[0]}
            return cls([cls.__CLASS__(**{header: dict_[key] for key, header in headers.items()}) for dict_ in list_])
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")

    def push(self, *args):
        for arg in args:
            if not isinstance(arg, self.__CLASS__):
                raise TypeError("'%s' object is not an instance of %s" % (type(arg).__name__, self.__CLASS__))
            elif arg not in self:
                self.__objects.append(arg)

    def to_table(self, path, headers=True, delimiter=","):
        if _ispathlike(path):
            _list2table(
                path,
                [{_camel_case(key): value for key, value in item.__dict__.items()} for item in self.__objects],
                headers=headers,
                delimiter=delimiter
            )
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")
