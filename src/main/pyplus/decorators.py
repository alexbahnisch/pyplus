from datetime import datetime as _datetime
from functools import wraps as _wraps


def parser(method):
    @_wraps(method)
    def wrapped(string, **kwargs):
        if isinstance(string, bytes):
            output = method(string.decode(), **kwargs)
            return output.encode() if isinstance(output, str) else output
        elif isinstance(string, str):
            output = method(string, **kwargs)
            return output.decode() if isinstance(output, bytes) else output
        else:
            raise TypeError("'%s' object is not a string" % type(string).__name__)

    return wrapped


def spliter(method):
    @_wraps(method)
    def wrapped(string, **kwargs):
        if string is None:
            return []
        elif isinstance(string, (float, int)) and not isinstance(string, bool):
            return [string]
        elif isinstance(string, bytes):
            items = method(string.decode(), **kwargs)
            return [item.encode() if isinstance(item, str) else item for item in items]
        elif isinstance(string, str):
            items = method(string, **kwargs)
            return [item.decode() if isinstance(item, bytes) else item for item in items]
        else:
            raise TypeError("'%s' object is not a string" % type(string).__name__)

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
