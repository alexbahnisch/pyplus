#!/usr/bin/env python
from copy import deepcopy as _deepcopy
from io import IOBase as _IOBase
from json import load as _load, loads as _loads
from pathlib import Path as _Path

from past.builtins import basestring as _basestring

from .common import ismappable as _ismappable, issequence as _issequence
from .lazy import LazyPath as _LazyPath


# noinspection PyPep8Naming,PyMethodParameters
class json(dict):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("json expected at most 1 arguments, got %s" % len(args))

        if len(args) > 0 and isinstance(args[0], dict):
            for key, value in args[0].items():
                if str(key) not in kwargs:
                    kwargs[str(key)] = value

        elif len(args) > 0 and hasattr(args[0], "__iter__"):
            for inx, items in enumerate(args[0]):
                if _ismappable(items):
                    if str(items[0]) not in kwargs:
                        kwargs[str(items[0])] = items[1]
                elif _issequence(items) and len(items) > 2:
                    raise ValueError("json update sequence element #%s has length %s; 2 is required" % inx, len(items))
                else:
                    raise TypeError("cannot convert json update sequence element #%s to a sequence" % inx)

        elif len(args) > 0:
            raise TypeError("'%s' object is not iterable" % type(args[0]).__name__)

        super(json, self).__init__(kwargs)

    def __copy__(self):
        return type(self)(self)

    def __deepcopy__(self,  memo):
        kwargs = {key: _deepcopy(value) for key, value in self.items()}
        return type(self)(kwargs)

    def __getattr__(self, key):
        return self.__getitem__(str(key))

    def __getitem__(self, key):
        return super(json, self).get(str(key))

    def __setattr__(self, key, value):
        self.__setitem__(str(key), value)

    def __setitem__(self, key, value):
        return super(json, self).__setitem__(str(key), value)

    @classmethod
    def from_dict(cls, dict_):
        assert isinstance(dict_, dict)
        output = cls()
        for key, value in dict_.items():
            output[key] = cls.from_object(value)

        return output

    @classmethod
    def from_list(cls, list_):
        assert isinstance(list_, list)
        output = []
        for element in list_:
            output.append(cls.from_object(element))

        return output

    @classmethod
    def from_object(cls, obj):
        if isinstance(obj, dict):
            return cls.from_dict(obj)
        elif isinstance(obj, list):
            return cls.from_list(obj)
        else:
            return obj

    @classmethod
    def from_path(cls, path):
        assert isinstance(path, _Path) or isinstance(path, _basestring)

        with _LazyPath(str(path)).read() as tmp_file:
            rv = cls.from_text(tmp_file)

        return rv

    @classmethod
    def from_string(cls, string):
        assert isinstance(string, _basestring)
        var = _loads(string)
        if isinstance(var, dict):
            return cls.from_dict(var)
        elif isinstance(var, list):
            return cls.from_list(var)
        else:
            return var

    @classmethod
    def from_text(cls, text):
        assert isinstance(text, _IOBase)
        var = _load(text)
        if isinstance(var, dict):
            return cls.from_dict(var)
        elif isinstance(var, list):
            return cls.from_list(var)
        else:
            return var

    def assign(self, *others, mutate=True):
        assert all(isinstance(other, type(self)) for other in others)
        rarg = self if mutate else self.copy()

        for other in others:
            for keys, values in other.items():
                rarg[keys] = other

        return rarg

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__({})

    def merge(self, *others):
        assert all(isinstance(other, type(self)) for other in others)
        pass  # TODO - finish
