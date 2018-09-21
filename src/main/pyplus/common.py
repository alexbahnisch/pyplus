"""
A collection of common helper functions that check if an object has characteristics of other objects.
"""
from decimal import Decimal as _Decimal
from os import name as _name
from pathlib import Path as _Path


def isintlike(value):
    """
    Checks if an object can be converted to an integer.
    @param value: {object} The object to check.
    @return {bool} Returns true an object can be converted to an integer.
    """
    try:
        int(value)
        return True
    except (TypeError, ValueError):
        return False


def isiterable(value, include_strings=True):
    """
    Checks if an object is iterable.
    @param value: {object} The object to check.
    @param include_strings: {bool} Include strings as an iterable type.
    @return {bool} Returns true if an object can be iterated.
    """
    if include_strings:
        return hasattr(value, "__iter__")
    else:
        return not isinstance(value, str) and hasattr(value, "__iter__")


def islistlike(value):
    """
    Checks if an object has list like properties, i.e has a length, is iterable, can get and set items.
    @param value: {object} The object to check.
    @return {bool} Returns true if an object is like a list.
    """
    return hasattr(value, "__len__") and hasattr(value, "__getitem__") and hasattr(value, "__setitem__") and isiterable(value)


def isnumber(value):
    """
    Checks if an object is a number, excludes booleans.
    @param value: {object} The object to check.
    @return {bool} Returns true if an object is/extends a builtin number.
    """
    return isinstance(value, (_Decimal, float, int)) and not isinstance(value, bool)


def ispair(value):
    """
    Checks if an object is a pair, i.e is iterable and has a length of 2.
    @param value: {object} The object to check.
    @return {bool} Returns true if an object is a pair.
    """
    return hasattr(value, "__len__") and len(value) == 2 and isiterable(value)


def ismappable(value):
    """
    Checks if an object is mappable, i.e can be passed into a 'dict' constructor.
    @param value: {object} The object to check.
    @return {bool} Returns true if the value is mappable.
    """
    return isinstance(value, dict) or (isiterable(value) and all(ispair(item) for item in value))


def ispathlike(value):
    """
    Checks if an object has path like properties, i.e. is/extends a string or pathlib.Path.
    @param value: {object} The object to check.
    @return {bool} Returns true if an object is path like.
    """
    return isinstance(value, (bytes, str, _Path))


def issequence(value):
    """
    Checks if an object has a length and is iterable.
    @param value: {object} The object to check.
    @return {bool} Returns true if an object is a sequence.
    """
    return hasattr(value, "__len__") and isiterable(value)


def istuplike(value):
    """
    Checks if an object has tuple like properties, i.e has a length, is iterable and can get items.
    @param value: {object} The object to check.
    @return {bool} Returns true if an object is like a tuple.
    """
    return hasattr(value, "__len__") and hasattr(value, "__getitem__") and isiterable(value)


def iswindows():
    """
    Checks if the current operating system is windows.
    @return {bool} Returns true if running on Windows or Ming-w32/64
    """
    return _name == "nt"


def iterable(value):
    """
    @deprecated will be remove next minor
    """
    if isiterable(value):
        return value
    else:
        return [value]
