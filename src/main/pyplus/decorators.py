#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime as _datetime
from functools import wraps as _wraps


def time(logger=print):
    def wrapper(method):
        @_wraps(method)
        def wrapped(*args, **kwargs):
            start = _datetime.now()
            output = method(*args, **kwargs)
            logger("Ran '%s' method in %s" % (method.__name__, _datetime.now() - start))
            return output
        return wrapped
    return wrapper
