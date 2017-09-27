from datetime import datetime as _datetime
from functools import wraps as _wraps

from .singleton import singleton


def decorator(method):
    if callable(method):
        @_wraps(method)
        def wrapped(*args, **kwargs):
            return method(*args, **kwargs)

        return wrapped

    else:
        raise TypeError("'%s' object is not callable" % type(method))


@decorator
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


@decorator
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


@singleton
class Timer:
    def __init__(self, logger=print, disabled=False):
        self.__disabled = bool(disabled)
        self.__level = 0
        self.__logger = logger

    def disable(self):
        self.__disabled = True

    def enable(self):
        self.__disabled = False

    @decorator
    def __call__(self, method):
        if self.__disabled:
            return method

        else:
            @_wraps(method)
            def wrapped(*args, **kwargs):
                start = _datetime.now()
                output = method(*args, **kwargs)
                self.__logger(_datetime.now() - start)
                return output

            return wrapped

    @decorator
    def plus(self, method):
        if self.__disabled:
            return method

        else:
            @_wraps(method)
            def wrapped(*args, **kwargs):
                start = _datetime.now()
                self.__logger(self.__level * "  " + "%s starting %s ..." % (start, method.__name__))
                self.__level += 1

                output = method(*args, **kwargs)
                self.__level -= 1

                end = _datetime.now()
                self.__logger(
                    self.__level * "  " + "... %s finished %s, completed in %s" % (end, method.__name__, end - start))
                return output

            return wrapped
