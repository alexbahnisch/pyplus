#!/usr/bin/env python
from future.utils import with_metaclass


def point():
    pass


class DataObjectMeta(type):
    __HEADERS__ = []

    @classmethod
    def from_array(mcs, array):
        assert isinstance(array, list)
        return mcs(*array)

    @classmethod
    def from_json(mcs, json):
        assert isinstance(json, dict)
        if mcs.__HEADERS__:
            return mcs(*[json[key] for key in mcs.__HEADERS__])
        else:
            return mcs(**json)


def dataobject(*headers):
    assert all(isinstance(header, str) for header in headers)

    def wrapper(class_):

        class Wrapper(with_metaclass(DataObjectMeta, class_)):
            __name__ = class_.__name__
            __HEADERS__ = list(headers)

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        return Wrapper

    return wrapper


def dataobjects(data_object_class):
    assert isinstance(data_object_class, DataObjectMeta)

    def wrapper(class_arg):
        class DataObjects(class_arg):
            __name__ = class_arg.__name__
            __CLASS__ = data_object_class

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        return DataObjects

    return wrapper


@dataobject("id")
class Object(object):

    @classmethod
    def class_method(cls):
        return "%s_class_method" % cls.__name__

    @property
    def prop(self):
        return "%s_property" % self.__class__.__name__

    @staticmethod
    def static_method():
        return "static_method"


if __name__ == "__main__":
    obj = Object()
    point()
