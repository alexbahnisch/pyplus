#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime as _datetime
from functools import wraps as _wraps

from past.builtins import unicode as _unicode


def parser(method):
    @_wraps(method)
    def wrapped(string, **kwargs):
        if isinstance(string, bytes):
            output = method(string.decode(), **kwargs)
            return output.encode() if isinstance(output, _unicode) else output
        elif isinstance(string, _unicode):
            return method(string)
        else:
            raise TypeError("TODO - raise better exception")

    return wrapped


def timer(logger=print, disabled=False):
    if disabled:
        def wrapper(method):
            return method
        return wrapper

    else:
        def wrapper(method):
            @_wraps(method)
            def wrapped(*args, **kwargs):
                start = _datetime.now()
                output = method(*args, **kwargs)
                logger(_datetime.now() - start)
                return output
            return wrapped
        return wrapper
