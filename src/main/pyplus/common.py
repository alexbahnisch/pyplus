"""
A collection of common helper functions to check if an object has characteristics of other objects.
"""
from decimal import Decimal as _Decimal
from os import name as _name
from pathlib import Path as _Path


def isintlike(obj):
    """
    Checks if an object can be converted to an integer
    """
    try:
        int(obj)
        return True
    except (TypeError, ValueError):
        return False


def isiterable(obj, include_strings=True):
    """
    Checks if an object is iterable
    """
    if include_strings:
        return hasattr(obj, "__iter__") or isinstance(obj, str)
    else:
        return not isinstance(obj, str) and hasattr(obj, "__iter__")


def islistlike(obj):
    """
    Checks if an object has tuple like properties, i.e has a length, is iterable, can get and set items
    """
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and hasattr(obj, "__setitem__") and isiterable(obj)


def isnumber(obj):
    """
    Checks if an object is a number, excludes booleans
    """
    return isinstance(obj, (_Decimal, float, int)) and not isinstance(obj, bool)


def ispair(obj):
    """
    Checks if an object is a pair, i.e is iterable and has a length of 2
    """
    return hasattr(obj, "__len__") and len(obj) == 2 and isiterable(obj)


def ismappable(obj):
    """
    Checks if an object is mappable, i.e can be passed into a 'dict' constructor
    """
    return isinstance(obj, dict) or (isiterable(obj) and all(ispair(item) for item in obj))


def ispathlike(obj):
    """
    Checks if an object has path like properties, i.e. is an instance of a string or pathlib.Path
    """
    return isinstance(obj, (bytes, str, _Path))


def issequence(obj):
    """
    Checks if an object has a length and is iterable
    """
    return hasattr(obj, "__len__") and isiterable(obj)


def istuplike(obj):
    """
    Checks if an object has tuple like properties, i.e has a length, is iterable and can get items
    """
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and isiterable(obj)


def iswindows():
    """
    Checks if the current operating system is windows
    """
    return _name == "nt"


def iterable(obj):
    """
    @deprecated will be remove next minor
    """
    if isiterable(obj):
        return obj
    else:
        return [obj]
