#!/usr/bin/env python
from copy import deepcopy as _deepcopy

from .io import csv2dict as _csv2dict
from .string import snake_case as _snake_case


class LazyObject(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __copy__(self):
        return self.__class__(**self.__dict__)

    def __deepcopy__(self, memo):
        kwargs = {key: _deepcopy(value) for key, value in self.__dict__.items()}
        return self.__class__(**kwargs)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, key))

    @classmethod
    def from_csv(cls, path):
        dict_ = _csv2dict(path)
        headers = {key: _snake_case(key) for key in dict_}
        rargs = []

        for item in zip(dict_[key] for key in dict_):
            rargs.append(cls(**{}))


class ImmutableLazyObject(LazyObject):

    def __setattr__(self, key, value):
        raise AttributeError("can't set attribute '%s' objects are immutable" % type(self).__name__)
