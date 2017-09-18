from .abstract import abstractclassmethod as _abstractclassmethod


# noinspection PyMethodParameters
class DataObjectMixin(object):
    __HEADERS__ = []

    @classmethod
    def from_list(cls, list_):
        assert isinstance(list_, list)
        return cls(*list_)

    @classmethod
    def from_dict(cls, dict_):
        assert isinstance(dict_, dict)
        return cls(*[dict_[key] for key in cls.__HEADERS__])

    @_abstractclassmethod
    def from_line(cls, line):
        pass


# noinspection PyPropertyDefinition
class DataObjectsMixin(object):
    __CLASS__ = DataObjectMixin

    def __init__(self):
        self.__objects = []
        self.init()

    def __getitem__(self, item):
        return self.__objects[item]

    def __iter__(self):
        return iter(self.__objects)

    def __len__(self):
        return len(self.__objects)

    def init(self):
        pass


def dataobject(*headers):
    assert all(isinstance(header, str) for header in headers)

    def wrapper(class_):
        if isinstance(class_, DataObjectMixin):
            class_.__HEADERS__ = list(headers)
            return class_

        else:
            class Wrapped(class_, DataObjectMixin):
                __name__ = class_.__name__
                __HEADERS__ = list(headers)

            return Wrapped

    return wrapper


def dataobjects(data_object_class):
    assert issubclass(data_object_class, DataObjectsMixin)

    def wrapper(class_):
        if issubclass(class_, DataObjectMixin):
            class_.__CLASS__ = data_object_class
            return class_

        else:
            class Wrapped(class_, DataObjectsMixin):
                __name__ = class_.__name__
                __CLASS__ = data_object_class

            return Wrapped

    return wrapper
