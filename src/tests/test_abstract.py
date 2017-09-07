#!/usr/bin/env python
from pyplus.abstract import abstractmethod, abstractclassmethod, abstractproperty, abstractstaticmethod
from pyplus.test import assert_exception


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


def test_abstract():
    obj = Abstract()

    assert_exception(
        Abstract.class_method, AttributeError,
        "abstract class method 'class_method' has not been overridden for 'Abstract' class"
    )

    assert_exception(
        obj.class_method, AttributeError,
        "abstract class method 'class_method' has not been overridden for 'Abstract' class"
    )

    assert_exception(
        lambda: obj.prop, AttributeError,
        "abstract property 'prop' has not been overridden for 'Abstract' class"
    )

    assert_exception(
        obj.static_method, AttributeError,
        "abstract static method 'static_method' has not been overridden"
    )

    assert_exception(
        obj.method, AttributeError,
        "abstract method 'method' has not been overridden for 'Abstract' class"
    )


def test_no_implementation():
    obj = NoImplementation()

    assert_exception(
        NoImplementation.class_method, AttributeError,
        "abstract class method 'class_method' has not been overridden for 'NoImplementation' class"
    )

    assert_exception(
        obj.class_method, AttributeError,
        "abstract class method 'class_method' has not been overridden for 'NoImplementation' class"
    )

    assert_exception(
        lambda: obj.prop, AttributeError,
        "abstract property 'prop' has not been overridden for 'NoImplementation' class"
    )

    assert_exception(
        obj.static_method, AttributeError,
        "abstract static method 'static_method' has not been overridden"
    )

    assert_exception(
        obj.method, AttributeError,
        "abstract method 'method' has not been overridden for 'NoImplementation' class"
    )


def test_correct_implementation():
    obj = CorrectImplementation()

    assert CorrectImplementation.class_method()

    assert obj.class_method()

    assert obj.method()

    assert obj.prop

    assert obj.static_method()


if __name__ == "__main__":
    test_abstract()
    test_no_implementation()
    test_correct_implementation()
