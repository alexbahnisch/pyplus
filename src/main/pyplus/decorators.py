"""
A collection of useful decorators.
"""
from datetime import datetime as _datetime
from functools import wraps as _wraps


def decorator(method):
    """
    @deprecated Will be changed next minor.
    """
    if callable(method):
        @_wraps(method)
        def wrapped(*args, **kwargs):
            return method(*args, **kwargs)

        return wrapped

    else:
        raise TypeError("'%s' object is not callable" % type(method).__name__)


@decorator
def parser(method):
    """
    Decorator for a string parsing function.
    Raises 'TypeError' if the first and only positional arg is not a string.
    Also guarantees if return value is a string, it is the same string as the input arg, i.e. byte or unicode.
    @param method: {function} Parser function, contains one positional arg and any number of keyword args.
    @return: {function} Wrapped parser function.
    """
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
    """
    Decorator for a string splitting function.
    Raises 'TypeError' if the first and only positional arg is not a string.
    Also guarantees if items in the return value list are strings, they are the same string as the input arg, i.e. byte or unicode.
    @param method: {function} Spliter function, contains one positional arg and any number of keyword args.
    @return: {function} Wrapped splitter function.
    """
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


class Timer:
    """
    Timer objects that can be used as decorators for functions which will log the start time, end time and duration of a function call.
    """
    def __init__(self, logger=print, disabled=False):
        """
        @param logger: {(arg: string) -> void} Function used to log timer information, by default it is 'print' so all information will go to std out.
        @param disabled: {bool} Is the initiated instance currently disabled.
        """
        self.__disabled = bool(disabled)
        self.__level = 0
        self.__logger = logger

    def disable(self):
        """
        Disable the timer.
        """
        self.__disabled = True

    def enable(self):
        """
        Enable the timer.
        """
        self.__disabled = False

    @decorator
    def __call__(self, method):
        """
        Decorates a function with basic timer logging, which will log the function call duration on completion.
        @param method: {function} Function/method to decorate with basic timer functionality.
        @return: {function} Wrapped function/method.
        """
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
        """
        Decorates a function with more advanced timer logging, which will log the start and end times, the function call duration on completion
        and will indent logs in relation to function scope.
        @param method: {function} Function/method to decorate with advanced timer functionality.
        @return: {function} Wrapped function/method.
        """
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


timer = Timer()
