from collections import OrderedDict as _OrderedDict
from copy import deepcopy as _deepcopy
from json import dump as _dump, dumps as _dumps, load as _load, loads as _loads

from . import common as _common
from .parse import create_lazy_parser
from .path import LazyPath as _LazyPath
from .string import alias2keys as _alias2keys


class _JsonMixin(object):
    def __getitem__(self, index):
        pass

    def __setitem__(self, key, value):
        pass

    def _merge(self, index, item):
        if (isinstance(self[index], Object) and isinstance(item, dict)) or (isinstance(self[index], Array) and isinstance(item, list)):
            self[index].merge(item.copy())
        else:
            self[index] = _deepcopy(item)

    def serialize(self, indent=2, sort_keys=True):
        return _dumps(self, indent=indent, sort_keys=sort_keys)

    def to_file(self, path, indent=2, sort_keys=True):
        with _LazyPath(str(path)).write() as tmp_file:
            _dump(self, tmp_file, indent=indent, sort_keys=sort_keys)


class Array(list, _JsonMixin):
    def __copy__(self):
        return type(self)(self)

    def __deepcopy__(self, memo):
        return type(self)(_deepcopy(item) for item in self)

    def __eq__(self, other):
        if isinstance(other, list) and len(self) == len(other):
            for index, item in enumerate(self):
                if item != other[index]:
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        if _common.isintlike(index) and 0 <= int(index) < self.length():
            return super(Array, self).__getitem__(int(index))
        else:
            return None

    def __setitem__(self, index, value):
        if _common.isintlike(index) and 0 <= int(index) < self.length():
            super(Array, self).__setitem__(int(index), value)
        elif _common.isintlike(index) and int(index) == self.length():
            self.append(value)
        elif _common.isintlike(index) and int(index) > self.length():
            self.extend([None] * (int(index) - self.length()) + [value])

    def length(self):
        return len(self)

    def assign(self, *others):
        if all(isinstance(other, list) for other in others):
            for other in others:
                for index, item in enumerate(other):
                    self[index] = item

            return self
        else:
            raise TypeError("assign(*others) arguments must be instances a 'list'")

    def concat(self, items):
        if _common.isiterable(items):
            rarg = self.copy()
            rarg.extend(items)
            return rarg
        else:
            rarg = self.copy()
            rarg.append(items)
            return rarg

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__({})

    def merge(self, *others):
        if all(isinstance(other, list) for other in others):
            for other in others:
                for index, item in enumerate(other):
                    self._merge(index, item)
            return self
        else:
            raise TypeError("merge(*others) arguments must be instances a 'list'")

    def push(self, *items):
        self.extend(items)
        return self.length()


# noinspection PyMethodOverriding
class Object(_OrderedDict, _JsonMixin):
    def __init__(self, *args, **kwargs):
        kwargs = _OrderedDict(kwargs)

        if len(args) == 1:
            if isinstance(args[0], dict):
                for key, value in args[0].items():
                    if str(key) not in kwargs:
                        kwargs[str(key)] = value

            elif _common.isiterable(args[0]):
                for inx, items in enumerate(args[0]):
                    if _common.ispair(items):
                        if str(items[0]) not in kwargs:
                            kwargs[str(items[0])] = items[1]
                    elif _common.issequence(items) and len(items) > 2:
                        raise ValueError("json update sequence element #%s has length %s; 2 is required" % inx, len(items))
                    else:
                        raise TypeError("cannot convert json update sequence element #%s to a sequence" % inx)

            else:
                raise TypeError("'%s' object is not iterable" % type(args[0]).__name__)

        elif len(args) > 1:
            raise TypeError("json expected at most 1 arguments, got %s" % len(args))

        super(Object, self).__init__(kwargs)

    def __contains__(self, key):
        return super(Object, self).__contains__(str(key))

    def __copy__(self):
        return type(self)(self)

    def __deepcopy__(self, memo):
        return type(self)({key: _deepcopy(value) for key, value in self.items()})

    def __eq__(self, other):
        if isinstance(other, dict) and self.keys() == other.keys():
            for key, value in other.items():
                if self[key] != value:
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattr__(self, key):
        return self.__getitem__(str(key))

    def __getitem__(self, key):
        return super(Object, self).get(str(key))

    def __len__(self):
        return len(self.keys())

    def __repr__(self):
        return dict.__repr__(self)

    def __setattr__(self, key, value):
        self.__setitem__(str(key), value)

    def __setitem__(self, key, value):
        return super(Object, self).__setitem__(str(key), value)

    def length(self):
        return len(self)

    def assign(self, *others):
        if all(isinstance(other, dict) for other in others):
            for other in others:
                for key, value in other.items():
                    self[key] = value

            return self
        else:
            raise TypeError("assign(*others) arguments must be instances of 'dict'")

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__({})

    def items(self, parser=False):
        if parser is False:
            return super().items()
        else:
            parser = create_lazy_parser(parser)
            return [(parser(key), value) for key, value in super().items()]

    def merge(self, *others):
        if all(isinstance(other, dict) for other in others):
            for other in others:
                for key, value in other.items():
                    self._merge(key, value)
            return self
        else:
            raise TypeError("merge(*others) arguments must be instances of 'dict'")


class JSON(object):
    __ARRAY__ = Array
    __OBJECT__ = Object

    @classmethod
    def from_file(cls, path, alias=None, errors=True):
        path, alias = _LazyPath(path), _alias2keys(alias) if alias is not None else []

        if path.exists():
            with path.read() as tmp_file:
                rarg = cls.from_collection(_load(tmp_file))

                for key in alias:
                    rarg = rarg[key]
                    if rarg is None:
                        return None

                return rarg

        else:
            if bool(errors):
                raise FileNotFoundError("[Errno 2] No such file or directory: '{}'".format(path))
            else:
                return None

    @classmethod
    def from_collection(cls, collection):
        if isinstance(collection, dict):
            return cls.__OBJECT__({key: cls.from_collection(value) for key, value in collection.items()})
        elif isinstance(collection, list):
            return cls.__ARRAY__(cls.from_collection(item) for item in collection)
        else:
            return collection

    @classmethod
    def parse(cls, string, errors=False):
        try:
            rarg = _loads(str(string))
            return cls.from_collection(rarg)

        except ValueError as error:
            if bool(errors):
                raise error
            else:
                return string
