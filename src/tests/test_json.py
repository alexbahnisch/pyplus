#!/usr/bin/env python
from pyplus.json import *
from pyplus.path import LazyPath
from pytest import raises

DIR = LazyPath(__file__)
ARRAY_INPUT = LazyPath(DIR.parent, "../resources/json/array.json")
SUB_ARRAY_OUTPUT = LazyPath(DIR.parent, "../resources/json/sub-array.json")
ARRAY_OUTPUT = LazyPath(DIR.parent, "../resources/json/array.zzz.json")
OBJECT_INPUT = LazyPath(DIR.parent, "../resources/json/object.json")
SUB_OBJECT_INPUT = DIR.parent.joinpath("../resources/json/sub-object.json")
OBJECT_OUTPUT = LazyPath(DIR.parent, "../resources/json/object.zzz.json")

DICT = {"1": 1, "2": 2}
DICT_INT = {1: 1, 2: 2}
LIST = [0, 1, 2, 3, 4]
LIST_STR = ["0", "1", "2", "3", "4"]
MAPPABLE = [("1", 1), ("2", 2)]
MAPPABLE_INT = [(1, 1), (2, 2)]
SET = {0, 1, 2, 3, 4}
STRING = "01234"
TUPLE = (0, 1, 2, 3, 4)


def test_array_alias():
    obj1 = JSON.from_file(ARRAY_INPUT, 0)
    obj2 = JSON.from_file(SUB_ARRAY_OUTPUT)
    assert obj1 == obj2
    assert obj1 is not obj2

    obj3 = JSON.from_file(ARRAY_INPUT, "[0].array")
    obj4 = JSON.from_file(SUB_ARRAY_OUTPUT, "array")
    assert obj3 == obj4
    assert obj3 is not obj4

    assert JSON.from_file(OBJECT_INPUT, "[0].doesNotExist") is None


def test_array_concat():
    array1, array2, array3 = Array(LIST), Array([0, 1, 2, 3, 4, 5]), Array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    assert array1.concat(5) == array2
    assert array1.concat([5, 6, 7, 8]) == array3
    assert array2.concat([6, 7, 8]) == array3


def test_array_copy():
    array1 = JSON.from_file(ARRAY_INPUT)
    array2 = array1.copy()

    assert array1 == array2
    assert array1 is not array2

    for index, item in enumerate(array1):
        assert item is array2[index]


def test_array_deepcopy():
    array1 = JSON.from_file(ARRAY_INPUT)
    array2 = array1.deepcopy()

    assert array1 == array2
    assert array1 is not array2

    for index, item in enumerate(array1):
        assert item == array2[index]
        assert item is not array2[index]


def test_array_eq():
    assert Array(LIST) == LIST
    assert Array(SET) == LIST
    assert Array(STRING) == LIST_STR
    assert Array(TUPLE) == LIST


def test_array_get():
    array = Array(LIST)
    assert array[0] is 0
    assert array[4] is 4
    assert array[-1] is None
    assert array[5] is None


def test_array_io():
    array = JSON.from_file(ARRAY_INPUT)
    array.to_file(ARRAY_OUTPUT)
    text1 = ARRAY_INPUT.read_text()
    text2 = ARRAY_OUTPUT.read_text()
    ARRAY_OUTPUT.delete()
    assert text1 == text2


def test_array_neq():
    assert Array(LIST) is not LIST
    assert Array(LIST) is not Array(LIST)
    assert Array(LIST) != Array(LIST_STR)
    assert Array(SET) != SET
    assert Array(STRING) != STRING
    assert Array(TUPLE) != TUPLE


def test_array_parse():
    text = ARRAY_INPUT.read_text()
    obj = JSON.from_file(ARRAY_INPUT)
    assert obj == JSON.parse(text)


def test_array_push():
    array1, array2, array3 = Array(LIST), Array([0, 1, 2, 3, 4, 5]), Array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    assert array1.push(5) is 6
    assert array1 == array2
    assert array1 is not array2
    assert array1.push(6, 7, 8) is 9
    assert array1 == array3
    assert array1 is not array3
    assert array2.push(6, 7, 8) is 9
    assert array2 == array3
    assert array2 is not array3


def test_array_set():
    array1, array2, array3 = Array(LIST), Array([1, 1, 2, 3, 4]), Array([1, 1, 2, 3, 4, None, None, None, 8])
    array1[0] = 1
    assert array1 == array2
    array1[-1] = 1
    assert array1 == array2
    array1[8] = 8
    assert array1 == array3


def test_array_serialize():
    text = ARRAY_INPUT.read_text()
    obj = JSON.from_file(ARRAY_INPUT)
    assert text == obj.serialize()


def test_json_io():
    assert JSON.from_file("dummyPath", errors=False) is None
    assert JSON.from_file("dummyPath", errors=False) is None

    with raises(FileNotFoundError, message="[Errno 2] No such file or directory: 'dummyPath'"):
        JSON.from_file("dummyPath")


def test_json_parse():
    obj = JSON.parse("string")
    assert obj == "string"

    with raises(ValueError):
        JSON.parse("string", True)


def test_object():
    with raises(TypeError, message="json expected at most 1 arguments, got 2"):
        Object(1, 2)

    with raises(TypeError, message="'int' object is not iterable"):
        Object(1)

    with raises(TypeError, message="cannot convert json update sequence element #0 to a sequence"):
        Object("string")

    with raises(TypeError, message="json update sequence element #0 has length 3; 2 is required"):
        Object([(1, 2, 3)])


def test_object_alias():
    obj1 = JSON.from_file(OBJECT_INPUT, "objects")
    obj2 = JSON.from_file(SUB_OBJECT_INPUT)
    assert obj1 == obj2
    assert obj1 is not obj2

    obj3 = JSON.from_file(OBJECT_INPUT, "objects[0]")
    obj4 = JSON.from_file(SUB_OBJECT_INPUT, 0)
    assert obj3 == obj4
    assert obj3 is not obj4

    assert JSON.from_file(OBJECT_INPUT, "objects[0].doesNotExist") is None


def test_object_assign():
    obj1 = JSON.from_file(OBJECT_INPUT)
    obj2 = JSON.from_file(OBJECT_INPUT)
    obj3 = Object().assign(obj1, obj2)

    assert obj1 == obj2
    assert obj1 is not obj2
    assert obj1 == obj3
    assert obj1 is not obj3

    for key, value in obj3.items():
        assert value == obj1[key]
        assert value is not obj1[key]
        assert value is obj2[key]

    obj4 = obj1.assign(obj2)

    assert obj1 is obj4
    assert obj3 == obj4
    assert obj3 is not obj4

    for key, value in obj4.items():
        assert value is obj3[key]
        assert value is obj2[key]


def test_object_assign_mutate():
    dict1 = {"key": {"key": "value"}}
    dict2 = {"key": ["item"]}

    obj1 = Object(dict1)
    obj2 = Object(dict2)
    obj3 = obj1.assign(obj2)

    assert obj1 == obj2
    assert obj1 is obj3
    assert obj2 == obj3
    assert obj2 is not obj3


def test_object_assign_pure():
    dict1 = {"key": {"key": "value"}}
    dict2 = {"key": ["item"]}

    obj1 = Object(dict1)
    obj2 = Object(dict2)
    obj3 = Object().assign(obj1, obj2)

    assert obj1 != obj2
    assert obj1 != obj3
    assert obj2 == obj3
    assert obj2 is not obj3


def test_object_contains():
    assert "1" in Object(DICT)
    assert 1 in Object(DICT)
    assert "3" not in Object(DICT)
    assert 3 not in Object(DICT)


def test_object_copy():
    obj1 = JSON.from_file(OBJECT_INPUT)
    obj2 = obj1.copy()

    assert obj1 == obj2
    assert obj1 is not obj2

    for key, value in obj1.items():
        assert value is obj2[key]


def test_object_deepcopy():
    obj1 = JSON.from_file(OBJECT_INPUT)
    obj2 = obj1.deepcopy()

    assert obj1 == obj2
    assert obj1 is not obj2

    for key, value in obj1.items():
        assert value == obj2[key]
        assert value is not obj2[key]


def test_object_eq():
    assert Object(DICT) == DICT
    assert Object(DICT_INT) == DICT
    assert Object(MAPPABLE) == DICT


def test_object_get():
    obj = Object({"key": 1})
    assert obj.key is 1
    assert obj.none is None


def test_object_io():
    obj = JSON.from_file(OBJECT_INPUT)
    obj.to_file(OBJECT_OUTPUT)
    text1 = OBJECT_INPUT.read_text()
    text2 = OBJECT_OUTPUT.read_text()
    OBJECT_OUTPUT.delete()
    assert text1 == text2


def test_object_items():
    obj = Object(DICT_INT)
    assert all(item in MAPPABLE for item in obj.items())
    assert all(item in MAPPABLE_INT for item in obj.items(parser=True))
    assert all(item in MAPPABLE_INT for item in obj.items(parser=int))


def test_object_ne():
    assert Object(DICT) is not DICT
    assert Object(DICT_INT) != DICT_INT
    assert Object(MAPPABLE) != MAPPABLE


def test_object_parse():
    text = OBJECT_INPUT.read_text()
    obj = JSON.from_file(OBJECT_INPUT)
    assert obj == JSON.parse(text)


def test_object_repr():
    dict_ = {"key": "value"}
    obj = Object(dict_)
    assert repr(dict_) == repr(obj)


def test_object_set():
    obj = Object({"key": 1})
    obj.key = 2
    obj.new = 1
    assert obj.key is 2
    assert obj.new is 1


def test_object_serialize():
    text = OBJECT_INPUT.read_text()
    obj = JSON.from_file(OBJECT_INPUT)
    assert text == obj.serialize()
