#!/usr/bin/env python


def isintlike(obj):
    return isinstance(obj, int) or (hasattr(obj, "__int__") and isinstance(int(obj), int))


def isiterable(obj):
    return hasattr(obj, "__iter__")


def islistlike(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and \
           hasattr(obj, "__iter__") and hasattr(obj, "__setitem__")


def ismappable(obj):
    return hasattr(obj, "__len__") and len(obj) == 2 and hasattr(obj, "__getitem__")


def issequence(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__")


def istuplike(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and hasattr(obj, "__iter__")


def iterable(obj):
    if isiterable(obj):
        return obj
    else:
        return [obj]
