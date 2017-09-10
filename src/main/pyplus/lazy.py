#!/usr/bin/env python
from copy import deepcopy


class LazyObject(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __copy__(self):
        return self.__class__(**self.__dict__)

    def __deepcopy__(self, memo):
        kwargs = {key: deepcopy(value) for key, value in self.__dict__.items()}
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


class ImmutableLazyObject(LazyObject):

    def __setattr__(self, key, value):
        raise AttributeError("can't set attribute '%s' objects are immutable" % type(self).__name__)
