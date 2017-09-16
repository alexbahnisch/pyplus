#!/usr/bin/env python
from past.builtins import basestring as _basestring


def isintlike(obj):
    try:
        int(obj)
        return True
    except (TypeError, ValueError):
        return False


def isiterable(obj):
    return hasattr(obj, "__iter__") or isinstance(obj, _basestring)


def islistlike(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and hasattr(obj, "__setitem__") and isiterable(obj)


def ispair(obj):
    return hasattr(obj, "__len__") and len(obj) == 2 and isiterable(obj)


def ismappable(obj):
    return isinstance(obj, dict) or (isiterable(obj) and all(ispair(item) for item in obj))


def issequence(obj):
    return hasattr(obj, "__len__") and isiterable(obj)


def isstringlike(obj):
    return isinstance(obj, _basestring) or (hasattr(obj, "__str__") and isinstance(str(obj), str))


def istuplike(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and hasattr(obj, "__iter__")


def iterable(obj):
    if isiterable(obj):
        return obj
    else:
        return [obj]
