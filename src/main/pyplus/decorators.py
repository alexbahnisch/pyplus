#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime as _datetime
from functools import wraps as _wraps

from past.builtins import unicode as _unicode


def parser(method):
    @_wraps(method)
    def wrapped(*args, **kwargs):
        if isinstance(args[0], bytes):
            args = (args[0].decode(), *args[1:len(args) + 1])
            output = method(*args, **kwargs)
            return output.encode() if isinstance(output, _unicode) else output
        elif isinstance(args[0], _unicode):
            output = method(*args, **kwargs)
            return output.decode() if isinstance(output, bytes) else output
        else:
            raise TypeError("'%s' object is not a string" % type(args[0]).__name__)

    return wrapped


def spliter(method):
    @_wraps(method)
    def wrapped(*args, **kwargs):
        if isinstance(args[0], bytes):
            args = (args[0].decode(), *args[1:len(args) + 1])
            items = method(*args, **kwargs)
            return [item.encode() if isinstance(item, _unicode) else item for item in items]
        elif isinstance(args[0], _unicode):
            items = method(*args, **kwargs)
            return [item.decode() if isinstance(item, bytes) else item for item in items]
        else:
            raise TypeError("'%s' object is not a string" % type(args[0]).__name__)

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
