#!/usr/bin/env python
from copy import copy as _copy, deepcopy as _deepcopy
from json import dump as _dump, dumps as _dumps, load as _load, loads as _loads
from pathlib import Path as _Path

from past.builtins import basestring as _basestring

from .common import (
    isintlike as _isintlike, isiterable as _isiterable, ismappable as _ismappable, issequence as _issequence
)
from .lazy import LazyPath as _LazyPath


class _JsonMixin(object):

    def stringify(self):
        return _dumps(self)

    def to_file(self, path):
        assert isinstance(path, _Path) or isinstance(path, _basestring)
        with _LazyPath(str(path)).write() as tmp_file:
            _dump(self, tmp_file)


class Array(list, _JsonMixin):

    def __copy__(self):
        return type(self)(self)

    def __deepcopy__(self, memo):
        return type(self)(_deepcopy(item) for item in self)

    def __getitem__(self, index):
        if _isintlike(index) and 0 <= int(index) < len(self):
            return super(Array, self).__getitem__(int(index))
        else:
            return None

    def __setitem__(self, index, value):
        if _isintlike(index) and 0 <= int(index) < len(self):
            super(Array, self).__setitem__(int(index), value)
        elif _isintlike(index) and int(index) < len(self):
            self.push([None] * (int(index) - len(self)), value)

    def concat(self, items):
        if _isiterable(items):
            return _copy(self).extend(items)
        else:
            return _copy(self).append(items)

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__({})

    def push(self, *items):
        return self.append(items)


class Object(dict, _JsonMixin):

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

        super(Object, self).__init__(kwargs)

    def __contains__(self, key):
        return super(Object, self).__contains__(str(key))

    def __copy__(self):
        return type(self)(self)

    def __deepcopy__(self, memo):
        return type(self)({key: _deepcopy(value) for key, value in self.items()})

    def __getattr__(self, key):
        return self.__getitem__(str(key))

    def __getitem__(self, key):
        return super(Object, self).get(str(key))

    def __setattr__(self, key, value):
        self.__setitem__(str(key), value)

    def __setitem__(self, key, value):
        return super(Object, self).__setitem__(str(key), value)

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


class JSON(object):
    __ARRAY__ = Array
    __OBJECT__ = Object

    @classmethod
    def from_dict(cls, dict_):
        assert isinstance(dict_, dict)
        return cls.__OBJECT__({key: cls.from_object(value) for key, value in dict_.items()})

    @classmethod
    def from_list(cls, list_):
        assert isinstance(list_, list)
        return cls.__ARRAY__(cls.from_object(item) for item in list_)

    @classmethod
    def from_file(cls, path):
        assert isinstance(path, _Path) or isinstance(path, _basestring)
        with _LazyPath(str(path)).read() as tmp_file:
            return cls.from_object(_load(tmp_file))

    @classmethod
    def from_object(cls, obj):
        if isinstance(obj, dict):
            return cls.from_dict(obj)
        elif isinstance(obj, list):
            return cls.from_list(obj)
        else:
            return obj

    @classmethod
    def parse(cls, string):
        assert isinstance(string, _basestring)
        rarg = _loads(string)
        if isinstance(rarg, dict):
            return cls.from_dict(rarg)
        elif isinstance(rarg, list):
            return cls.from_list(rarg)
        else:
            return rarg
