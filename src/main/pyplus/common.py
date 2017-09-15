#!/usr/bin/env python
from past.builtins import basestring as _basestring


def isintlike(obj):
    return isinstance(obj, int) or hasattr(obj, "__int__")


def isiterable(obj):
    return hasattr(obj, "__iter__")


def islistlike(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and \
           hasattr(obj, "__iter__") and hasattr(obj, "__setitem__")


def ispair(obj):
    return hasattr(obj, "__len__") and len(obj) == 2 and hasattr(obj, "__getitem__")


def ismappable(obj):
    return isinstance(obj, dict) or (isiterable(obj) and all(ispair(item) for item in obj))


def issequence(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__")


def isstringlike(obj):
    return isinstance(obj, _basestring) or (hasattr(obj, "__str__") and isinstance(str(obj), str))


def istuplike(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and hasattr(obj, "__iter__")


def iterable(obj):
    if isiterable(obj):
        return obj
    else:
        return [obj]
