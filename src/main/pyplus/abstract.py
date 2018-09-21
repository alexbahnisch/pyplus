"""
A collection of lazy abstract decorators that will only raise an exception when the decorated method is called before
being overridden, instead of on initiation of a subclass instance.
"""
from functools import wraps as _wraps


def abstractclassmethod(method):
    """
    A lazy alternative to the `abc.abstractclassmethod`.
    @param method: {classmethod} An empty/unreachable class method.
    @return: {classmethod} An abstract class method that will raise an exception when called.
    """
    # noinspection PyUnusedLocal
    @_wraps(method)
    def wrapped(cls, *args, **kwargs):
        raise AttributeError(
            "abstract class method '%s' has not been overridden for '%s' class" % (method.__name__, cls.__name__)
        )

    return classmethod(wrapped)


def abstractproperty(method):
    """
    @deprecated will be remove next minor
    """
    @_wraps(method)
    def wrapped(self):
        raise AttributeError(
            "abstract property '%s' has not been overridden for '%s' class" % (method.__name__, type(self).__name__)
        )

    return property(wrapped)


def abstractstaticmethod(method):
    """
    @deprecated will be remove next minor
    """
    # noinspection PyUnusedLocal
    @_wraps(method)
    def wrapped(*args, **kwargs):
        raise AttributeError("abstract static method '%s' has not been overridden" % method.__name__)

    return staticmethod(wrapped)


def abstractmethod(method):
    """
    A lazy alternative to the `abc.abstractmethod`.
    @param method: {method} An empty/unreachable method.
    @return: {method} An abstract method that will raise an exception when called.
    """
    # noinspection PyUnusedLocal
    @_wraps(method)
    def wrapped(self, *args, **kwargs):
        raise AttributeError(
            "abstract method '%s' has not been overridden for '%s' class" % (method.__name__, self.__class__.__name__)
        )

    return wrapped
