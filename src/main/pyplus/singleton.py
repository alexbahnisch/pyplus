"""
@deprecated will be remove next minor
"""


class Singleton(type):
    """
    @deprecated will be remove next minor
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def singleton(class_):
    """
    @deprecated will be remove next minor
    """
    class WrappedSingleton(class_, metaclass=Singleton):
        __name__ = class_.__name__

    return WrappedSingleton
