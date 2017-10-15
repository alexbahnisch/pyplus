#!/usr/bin/env python


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def singleton(class_):
    class WrappedSingleton(class_, metaclass=Singleton):
        __name__ = class_.__name__

    return WrappedSingleton
