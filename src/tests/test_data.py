#!/usr/bin/env python3
from pyplus.data import *
from pyplus.parse import parse
from pyplus.path import LazyPath
from pytest import raises


DIR = LazyPath(__file__)
CSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/csv/headers.csv")
CSV_HEADERS_OUTPUT = LazyPath(DIR.parent, "../resources/csv/headers.output.csv")
CSV_HEADERS_TEMP = LazyPath(DIR.parent, "../resources/csv/headers.temp.csv")
CSV_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/csv/headless.csv")
CSV_HEADLESS_OUTPUT = LazyPath(DIR.parent, "../resources/csv/headless.output.csv")
CSV_HEADLESS_TEMP = LazyPath(DIR.parent, "../resources/csv/headless.temp.csv")
TSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headers.tsv")
TSV_HEADERS_OUTPUT = LazyPath(DIR.parent, "../resources/tsv/headers.output.tsv")
TSV_HEADERS_TEMP = LazyPath(DIR.parent, "../resources/tsv/headers.temp.tsv")
TSV_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headless.tsv")
TSV_HEADLESS_OUTPUT = LazyPath(DIR.parent, "../resources/tsv/headless.output.tsv")
TSV_HEADLESS_TEMP = LazyPath(DIR.parent, "../resources/tsv/headless.temp.tsv")
TXT_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/txt/headless.txt")
TXT_HEADLESS_OUTPUT = LazyPath(DIR.parent, "../resources/txt/headless.output.txt")
TXT_HEADLESS_TEMP = LazyPath(DIR.parent, "../resources/txt/headless.temp.txt")


# noinspection PyShadowingBuiltins
@dataobject("bool", "int", "float", "string", "null")
class Object1(DataObjectMixin):
    def __init__(self, bool, int, float, string, null):
        self._bool = bool
        self._int = int
        self._float = float
        self._string = string
        self._null = null

    @classmethod
    def from_line(cls, line):
        assert isinstance(line, str)
        return cls(*map(parse, line.split(",")))

    def to_line(self):
        return ",".join(map(str, self.to_list()))


# noinspection PyShadowingBuiltins
@dataobject("bool", "int", "float", "string", "null")
class Object2:
    def __init__(self, bool, int, float, string, null):
        self._bool = bool
        self._int = int
        self._float = float
        self._string = string
        self._null = null


@dataobjects(Object1)
class Objects1(DataObjectsMixin):
    pass


@dataobjects(Object2)
class Objects2:
    pass


OBJECTS = Objects1([
    Object1(False, 1, 3.387182583, 'boring', None),
    Object1(False, 2, 4.523252832, 'royal', None),
    Object1(True, 3, 1.577410661, 'want', None),
    Object1(True, 4, 0.861610127, 'communicate', None),
    Object1(True, 5, 1.461357371, 'perfect', None),
    Object1(True, 6, 1.907316961, 'crack', None),
    Object1(True, 7, 1.214172801, 'ragged', None),
    Object1(False, 8, 2.010788362, 'scribble', None),
    Object1(True, 9, 1.91548151, 'obnoxious', None),
    Object1(True, 10, 0.785592075, 'incandescent', None)
])


def test_dataobject_eq():
    obj1 = Object1(False, 1, 3.387182583, "boring", None)
    obj2 = Object2.from_dict({"bool": False, "int": 1, "float": 3.387182583, "string": "boring", "null": None})

    assert obj1 == obj2
    assert obj1 is not obj2


def test_dataobject_exceptions():
    with raises(TypeError, message="'NoneType' object is not a instance of a dict"):
        Object2.from_dict(None)

    with raises(AttributeError, message="abstract class method 'from_line' has not been overridden for 'Class1' class"):
        Object2.from_line("")

    with raises(AttributeError, message="abstract method 'to_line' has not been overridden for 'Class1' class"):
        obj = Object2(False, 1, 3.387182583, "boring", None)
        obj.to_line()


def test_dataobject_ne():
    obj1 = Object1(False, 1, 3.387182583, "boring", None)
    obj2 = Object1(True, 1, 3.387182583, "boring", None)

    assert obj1 != obj2
    assert obj1 != 1


def test_dataobjects_exceptions():
    with raises(TypeError, message="dataobject() arguments must be strings"):
        dataobject(1)

    with raises(TypeError, message="dataobjects() argument must be a subclass of 'DataObjectMixin'"):
        dataobjects(object)

    with raises(TypeError, message="'path' argument must be a bytes or unicode string or pathlib.Path"):
        Objects1.from_table(None)

    with raises(TypeError, message="'path' argument must be a bytes or unicode string or pathlib.Path"):
        Objects1.from_txt_file(None)

    with raises(TypeError, message="'path' argument must be a bytes or unicode string or pathlib.Path"):
        Objects1().to_table(None)

    with raises(TypeError, message="'path' argument must be a bytes or unicode string or pathlib.Path"):
        Objects1().to_txt_file(None)


def test_dataobjects_table():
    objects1 = Objects1.from_table(CSV_HEADERS_INPUT)
    objects2 = Objects1.from_table(CSV_HEADLESS_INPUT, headers=False)
    objects3 = Objects2.from_table(TSV_HEADERS_INPUT, delimiter="\t")
    objects4 = Objects2.from_table(TSV_HEADLESS_INPUT, delimiter="\t", headers=False)

    assert OBJECTS == objects1
    assert OBJECTS == objects2
    assert OBJECTS == objects3
    assert OBJECTS == objects4

    objects1.to_table(CSV_HEADERS_TEMP)
    objects2.to_table(CSV_HEADLESS_TEMP, headers=False)
    objects1.to_table(TSV_HEADERS_TEMP, delimiter="\t")
    objects2.to_table(TSV_HEADLESS_TEMP, delimiter="\t", headers=False)

    assert CSV_HEADERS_OUTPUT.read_text() == CSV_HEADERS_TEMP.read_text()
    assert CSV_HEADLESS_OUTPUT.read_text() == CSV_HEADLESS_TEMP.read_text()
    assert TSV_HEADERS_OUTPUT.read_text() == TSV_HEADERS_TEMP.read_text()
    assert TSV_HEADLESS_OUTPUT.read_text() == TSV_HEADLESS_TEMP.read_text()


def test_dataobjects_txt():
    objects = Objects1.from_txt_file(TXT_HEADLESS_INPUT)
    objects.to_txt_file(TXT_HEADLESS_TEMP)

    assert OBJECTS == objects
    assert TXT_HEADLESS_OUTPUT.read_text() == TXT_HEADLESS_TEMP.read_text()
