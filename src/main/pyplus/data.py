"""
A collection of data driven object mixins and decorators.
"""
from .abstract import abstractclassmethod as _abstractclassmethod, abstractmethod as _abstractmethod
from .common import ispathlike as _ispathlike
from .json import Array as _Array, Object as _Object
from .object import LazyObjects as _LazyObjects
from .path import LazyPath as _LazyPath
from .string import snake_case as _snake_case
from .table import list2table as _list2table, table2list as _table2list


# noinspection PyMethodParameters
class DataObjectMixin:
    """
    A mixin to create data driven objects that can be easily serialized and deserialized.
    If used as super class, subclass must override '\_\_HEADER\_\_' attribute with a list of strings that represent an
    ordered dict key to '\_\_init\_\_' arg mapping.
    """
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
        """
        Deserialize object from a dict.
        @param arg: {dict}
        @return: {pyplus.data.DataObjectMixin}
        """
        if isinstance(arg, dict):
            # noinspection PyArgumentList
            return cls(*[arg[key] for key in cls.__HEADERS__])
        else:
            raise TypeError("'%s' object is not a instance of a dict" % type(arg).__name__)

    @_abstractclassmethod
    def from_line(cls, line):
        """
        Deserialize object from a line of text. Needs to be overridden to be used.
        @param line: {string}
        @return: {pyplus.data.DataObjectMixin}
        """
        pass

    def to_dict(self):
        """
        Serialize object to a dict.
        @return: {pyplus.json.Object}
        """
        temp_dict = {_snake_case(key): value for key, value in self.__dict__.items()}
        return _Object([(header, temp_dict[header]) for header in self.__HEADERS__])

    @_abstractmethod
    def to_line(self):
        """
        Serialize object to a line of text, needs to be overridden to be used.
        @return: {string}
        """
        pass

    def to_list(self):
        """
        Serialize object to a list.
        @return: {pyplus.json.Array}
        """
        temp_dict = {_snake_case(key): value for key, value in self.__dict__.items()}
        return _Array([temp_dict[header] for header in self.__HEADERS__])


# noinspection PyPropertyDefinition,PyArgumentList
class DataObjectsMixin(_LazyObjects):
    """
    A mixin to create a container of data driven objects that can be easily serialized and deserialized.
    If used as super class, subclass must override '\_\_CLASS\_\_' attribute with a subclass of DataObjectMixin.
    """
    __CLASS__ = DataObjectMixin

    def __init__(self, iterable=None):
        """
        @param iterable: {*DataObjectMixin} A iterable collection of DataObjectMixin instances.
        """
        super().__init__(iterable)
        self._init()

    def _init(self):
        """
        Method called after initialization, should be overridden with any post initialization processing.
        """
        pass

    @classmethod
    def from_table(cls, path, delimiter=",", headers=True, parse=True):
        """
        Deserialize object from a text delimited table, e.g. csv.
        @param path: {string or pathlib.Path}
        @param delimiter: {string}
        @param headers: {bool} Does the table contain headers.
        @param parse: {bool or function} Should strings be parsed (if bool) or parser (if function).
        @return: {pyplus.data.DataObjectsMixin}
        """
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
        """
        Deserialize object from a text file, from_line of '\_\_CLASS\_\_' needs to be overridden.
        @param path: {sting or pathlib.Path}
        @return: {pyplus.data.DataObjectsMixin}
        """
        if _ispathlike(path):
            with _LazyPath(path).read() as txt_file:
                return cls([cls.__CLASS__.from_line(txt_line) for txt_line in txt_file])
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")

    def to_table(self, path, delimiter=",", headers=True):
        """
        Serialize object to a text delimited table, e.g. csv.
        @param path: {string or pathlib.Path}
        @param delimiter: {string}
        @param headers: {bool} Write table headers.
        """
        if _ispathlike(path):
            _list2table(path, [item.to_dict() for item in self], headers=headers, delimiter=delimiter)
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")

    def to_txt_file(self, path):
        """
        Serialize object to a text file, to_line of '\_\_CLASS\_\_' needs to be overridden.
        @param path: {sting or pathlib.Path}
        """
        if _ispathlike(path):
            with _LazyPath(path).write() as txt_file:
                for obj in self:
                    txt_file.write(obj.to_line() + "\n")
        else:
            raise TypeError("'path' argument must be a bytes or unicode string or pathlib.Path")


def dataobject(*headers):
    """
    Class decorator to mixin DataObjectMixin to class.
    @param headers: {string[]} list of strings that represent an ordered dict key to '\_\_init\_\_' arg mapping.
    @return: {function} decorator that will create a subclass of the decorated class and DataObjectMixin
    """
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
    """
    Class decorator to mixin DataObjectsMixin to class.
    @param data_object_class: {type} Subclass of DataObjectMixin.
    @return: {function} decorator that will create a subclass of the decorated class and DataObjectsMixin
    """
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
