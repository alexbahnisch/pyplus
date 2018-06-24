from .abstract import abstractclassmethod as _abstractclassmethod, abstractmethod as _abstractmethod
from .common import ispathlike as _ispathlike
from .json import Array as _Array, Object as _Object
from .object import LazyObjects as _LazyObjects
from .path import LazyPath as _LazyPath
from .string import snake_case as _snake_case
from .table import list2table as _list2table, table2list as _table2list


# noinspection PyMethodParameters
class DataObjectMixin:
    __HEADERS__ = []

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_dict(cls, arg):
        if isinstance(arg, dict):
            # noinspection PyArgumentList
            return cls(*[arg[key] for key in cls.__HEADERS__])
        else:
            raise TypeError("'%s' object is not a instance of a dict" % type(arg).__name__)

    @_abstractclassmethod
    def from_line(cls, line):
        pass

    def to_dict(self):
        temp_dict = {_snake_case(key): value for key, value in self.__dict__.items()}
        return _Object([(header, temp_dict[header]) for header in self.__HEADERS__])

    @_abstractmethod
    def to_line(self):
        pass

    def to_list(self):
        temp_dict = {_snake_case(key): value for key, value in self.__dict__.items()}
        return _Array([temp_dict[header] for header in self.__HEADERS__])


# noinspection PyPropertyDefinition,PyArgumentList
class DataObjectsMixin(_LazyObjects):
    __CLASS__ = DataObjectMixin

    def __init__(self, iterable=None):
        super().__init__(iterable)
        self._init()

    def _init(self):
        pass

    @classmethod
    def from_table(cls, path, delimiter=",", headers=True, parse=True):
        if _ispathlike(path):
            array = _table2list(path, delimiter=delimiter, headers=headers, parse=parse)
            if headers:
                return cls([cls.__CLASS__.from_dict(obj) for obj in array])
            else:
                return cls([cls.__CLASS__(*obj.values()) for obj in array])
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")

    @classmethod
    def from_txt_file(cls, path):
        if _ispathlike(path):
            with _LazyPath(path).read() as txt_file:
                return cls([cls.__CLASS__.from_line(txt_line) for txt_line in txt_file])
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")

    def to_table(self, path, delimiter=",", headers=True):
        if _ispathlike(path):
            _list2table(path, [item.to_dict() for item in self], headers=headers, delimiter=delimiter)
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")

    def to_txt_file(self, path):
        if _ispathlike(path):
            with _LazyPath(path).write() as txt_file:
                for obj in self:
                    txt_file.write(obj.to_line() + "\n")
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")


def dataobject(*headers):
    if all(isinstance(header, str) for header in headers):
        def wrapper(class_):
            if issubclass(class_, DataObjectMixin):
                class_.__HEADERS__ = list(headers)
                return class_

            else:
                class Wrapped(class_, DataObjectMixin):
                    __name__ = class_.__name__
                    __HEADERS__ = list(headers)

                return Wrapped

        return wrapper
    else:
        raise TypeError("dataobject(*headers) arguments must be strings")


def dataobjects(data_object_class):
    if issubclass(data_object_class, DataObjectMixin):
        def wrapper(class_):
            if issubclass(class_, DataObjectsMixin):
                class_.__CLASS__ = data_object_class
                return class_

            else:
                class Wrapped(class_, DataObjectsMixin):
                    __name__ = class_.__name__
                    __CLASS__ = data_object_class

                return Wrapped

        return wrapper
    else:
        raise TypeError("dataobjects(data_object_class) argument must be a subclass of 'DataObjectMixin'")
