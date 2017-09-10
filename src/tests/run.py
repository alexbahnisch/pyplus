#!/usr/bin/env python
from pyplus.abstract import abstractmethod, abstractclassmethod, abstractproperty, abstractstaticmethod


class Abstract():
    __TRUE__ = True

    @abstractmethod
    def method(self):
        pass

    @abstractclassmethod
    def class_method(cls):
        pass

    @abstractproperty
    def prop(self):
        pass

    @abstractstaticmethod
    def static_method():
        pass


class Class(Abstract):
    __TRUE__ = True

    def method(self):
        return self.__TRUE__

    @classmethod
    def class_method(cls):
        return cls.__TRUE__

    def prop(self):
        return self.__TRUE__

    @staticmethod
    def static_method():
        return True


def fun():
    pass


def test_abstract():
    obj = Class()

    method = obj.method
    print(method(), obj.method())

    class_method = Class.class_method
    print(class_method(), Class.class_method())

    class_method = obj.class_method
    print(class_method(), obj.class_method())

    print(obj.prop, obj.prop())

    static_method = obj.static_method
    print(static_method(), obj.static_method())


def tests_set():
    pass


if __name__ == "__main__":
    tests_set()
