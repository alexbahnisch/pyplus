#!/usr/bin/env python
from .abstract import abstractclassmethod


class DataObjectMixin(object):
    __HEADERS__ = []

    @classmethod
    def from_array(cls, array):
        assert isinstance(array, list)
        return cls(*array)

    @classmethod
    def from_json(cls, json):
        assert isinstance(json, dict)
        return cls(*[json[key] for key in cls.__HEADERS__])

    @abstractclassmethod
    def from_line(cls, line):
        pass


# noinspection PyPropertyDefinition
class DataObjectsMixin(object):
    __CLASS__ = DataObjectMixin

    def __init__(self):
        self.__objects = []

    def __iter__(self):
        return iter(self.__objects)

    def __getitem__(self, item):
        return self.__objects[item]

    def __len__(self):
        return len(self.__objects)

    def process(self):
        pass


def dataobject(*headers):
    assert all(isinstance(header, str) for header in headers)

    def wrapper(class_):
        # noinspection PyAbstractClass,PyArgumentList
        class Wrapper(class_, DataObjectMixin):
            __name__ = class_.__name__
            __HEADERS__ = list(headers)

            def __init__(self, *args, **kwargs):
                super(Wrapper, self).__init__(*args, **kwargs)

        return Wrapper

    return wrapper


def dataobjects(data_object_class):
    assert isinstance(data_object_class, DataObjectsMixin)

    def wrapper(class_):
        class Wrapper(class_, DataObjectsMixin):
            __name__ = class_.__name__
            __CLASS__ = data_object_class

        return Wrapper

    return wrapper
