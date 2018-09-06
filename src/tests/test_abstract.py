#!/usr/bin/env python3
from pytest import raises

from pyplus.abstract import abstractmethod, abstractclassmethod, abstractproperty, abstractstaticmethod


# noinspection PyMethodParameters
class Abstract(object):
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


# noinspection PyAbstractClass
class NoImplementation(Abstract):
    pass


# noinspection PyMethodParameters
class IncorrectImplementation(Abstract):
    def method(self):
        return self.__TRUE__

    def class_method(cls):
        return cls.__TRUE__

    def static_method():
        return True

    def prop(self):
        return self.__TRUE__


class CorrectImplementation(Abstract):
    def method(self):
        return self.__TRUE__

    @classmethod
    def class_method(cls):
        return cls.__TRUE__

    @staticmethod
    def static_method():
        return True

    @property
    def prop(self):
        return self.__TRUE__


# noinspection PyStatementEffect
def test_abstract():
    obj = Abstract()

    with raises(AttributeError,
                message="abstract class method 'class_method' has not been overridden for 'Abstract' class"):
        Abstract.class_method()

    with raises(AttributeError,
                message="abstract class method 'class_method' has not been overridden for 'Abstract' class"):
        obj.class_method()

    with raises(AttributeError,
                message="abstract class method 'class_method' has not been overridden for 'Abstract' class"):
        obj.class_method()

    with raises(AttributeError, message="abstract property 'prop' has not been overridden for 'Abstract' class"):
        obj.prop

    with raises(AttributeError, message="abstract static method 'static_method' has not been overridden"):
        obj.static_method()

    with raises(AttributeError, message="abstract method 'method' has not been overridden for 'Abstract' class"):
        obj.method()


# noinspection PyStatementEffect
def test_no_implementation():
    obj = NoImplementation()

    with raises(AttributeError,
                message="abstract class method 'class_method' has not been overridden for 'NoImplementation' class"):
        NoImplementation.class_method()

    with raises(AttributeError,
                message="abstract class method 'class_method' has not been overridden for 'NoImplementation' class"):
        obj.class_method()

    with raises(AttributeError,
                message="abstract class method 'class_method' has not been overridden for 'NoImplementation' class"):
        obj.class_method()

    with raises(AttributeError,
                message="abstract property 'prop' has not been overridden for 'NoImplementation' class"):
        obj.prop

    with raises(AttributeError, message="abstract static method 'static_method' has not been overridden"):
        obj.static_method()

    with raises(AttributeError,
                message="abstract method 'method' has not been overridden for 'NoImplementation' class"):
        obj.method()


def test_correct_implementation():
    obj = CorrectImplementation()
    assert CorrectImplementation.class_method()
    assert obj.class_method()
    assert obj.method()
    assert obj.prop
    assert obj.static_method()
