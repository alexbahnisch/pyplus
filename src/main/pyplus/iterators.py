#!/usr/bin/env python


def iterable(obj):
    return hasattr(obj, "__iter__")


def iterate(obj):
    if iterable(obj):
        return obj
    else:
        return [obj]
