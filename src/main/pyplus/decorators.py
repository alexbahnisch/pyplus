#!/usr/bin/env python
from datetime import datetime as _datetime
from functools import wraps as _wraps


def abstractmethod(method):
    # noinspection PyUnusedLocal
    @_wraps(method)
    def wrapper(*args, **kwargs):
        raise NotImplementedError("Abstract method '%s' has not been overridden" % method.__name__)
    return wrapper


# noinspection PyShadowingBuiltins
def classmethod(method):
    @_wraps(method)
    def wrapper(cls, *args, **kwargs):
        if isinstance(cls, object):
            cls = cls.__class__
        return method(cls, *args, **kwargs)
    return wrapper


# noinspection PyShadowingBuiltins
def staticmethod(method):
    @_wraps(method)
    def wrapper(self, *args, **kwargs):
        return method(*args, **kwargs)
    return wrapper


def time(logger=print):
    def decorator(method):
        @_wraps(method)
        def wrapper(*args, **kwargs):
            start = _datetime.now()
            output = method(*args, **kwargs)
            logger("Ran '%s' method in %s" % (method.__name__, datetime.now() - start))
            return output
        return wrapper
    return decorator
