from functools import wraps as _wraps


def abstractclassmethod(method):
    # noinspection PyUnusedLocal
    @_wraps(method)
    def wrapped(cls, *args, **kwargs):
        raise AttributeError(
            "abstract class method '%s' has not been overridden for '%s' class" % (method.__name__, cls.__name__)
        )
    return classmethod(wrapped)


def abstractproperty(method):
    @_wraps(method)
    def wrapped(self):
        raise AttributeError(
            "abstract property '%s' has not been overridden for '%s' class" % (method.__name__, type(self).__name__)
        )
    return property(wrapped)


def abstractstaticmethod(method):
    # noinspection PyUnusedLocal
    @_wraps(method)
    def wrapped(*args, **kwargs):
        raise AttributeError("abstract static method '%s' has not been overridden" % method.__name__)
    return staticmethod(wrapped)


def abstractmethod(method):
    # noinspection PyUnusedLocal
    @_wraps(method)
    def wrapped(self, *args, **kwargs):
        raise AttributeError(
            "abstract method '%s' has not been overridden for '%s' class" % (method.__name__, self.__class__.__name__)
        )
    return wrapped
