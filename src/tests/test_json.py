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


def test_array_assign_mutate():
    arr1 = Array(["item1", "item2"])
    arr1_dc = arr1.deepcopy()
    arr2 = Array(["item1", {"key": "value"}])
    arr2_dc = arr2.deepcopy()
    arr3 = arr1.assign(arr2)

    assert arr1 != arr1_dc
    assert arr2 == arr2_dc
    assert arr1 == arr2
    assert arr1 is arr3
    assert arr2 == arr3
    assert arr2 is not arr3


def test_array_assign_pure():
    arr1 = Array(["item1", "item2"])
    arr1_dc = arr1.deepcopy()
    arr2 = Array(["item1", {"key": "value"}])
    arr2_dc = arr2.deepcopy()
    arr3 = Array().assign(arr1, arr2)

    assert arr1 == arr1_dc
    assert arr2 == arr2_dc
    assert arr2 == arr3
    assert arr2 is not arr3
    assert arr2[1] is arr3[1]


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


def test_array_exceptions():
    array = JSON.from_file(ARRAY_INPUT)

    with raises(TypeError, message="assign(*others) arguments must be instances of 'list'"):
        array.assign(None)

    with raises(TypeError, message="merge(*others) arguments must be instances of 'list'"):
        array.merge(None)


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


def test_array_merge_mutate():
    arr1 = JSON.from_collection([{"key1": "value1"}, {"key2": "value2"}])
    arr1_dc = arr1.deepcopy()
    arr2 = JSON.from_collection([{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}])
    arr2_dc = arr2.deepcopy()
    arr3 = JSON.from_collection([{"key1": "value1", "key2": "value2"}])
    arr3_dc = arr3.deepcopy()
    arr4 = JSON.from_collection([{"key1": "value1", "key2": "value2"}, {"key2": "value2"}, {"key3": "value3"}])
    arr5 = arr1.merge(arr2, arr3)

    assert arr1 != arr1_dc
    assert arr2 == arr2_dc
    assert arr3 == arr3_dc
    assert arr1 == arr4
    assert arr1 is not arr4
    assert arr1 == arr5
    assert arr1 is arr5
    assert arr5[0] == arr3[0]
    assert arr5[0] is not arr3[0]


def test_array_merge_pure():
    arr1 = JSON.from_collection([{"key1": "value1"}, {"key2": "value2"}])
    arr1_dc = arr1.deepcopy()
    arr2 = JSON.from_collection([{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}])
    arr2_dc = arr2.deepcopy()
    arr3 = JSON.from_collection([{"key1": "value1", "key2": "value2"}])
    arr3_dc = arr3.deepcopy()
    arr4 = JSON.from_collection([{"key1": "value1", "key2": "value2"}, {"key2": "value2"}, {"key3": "value3"}])
    arr5 = Array().merge(arr1, arr2, arr3)

    assert arr1 == arr1_dc
    assert arr2 == arr2_dc
    assert arr3 == arr3_dc
    assert arr4 == arr5
    assert arr4 is not arr5
    assert arr5[0] == arr3[0]
    assert arr5[0] is not arr3[0]


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
    obj = JSON.from_file(OBJECT_INPUT)
    assert obj.length() == 2
    obj.int = 1
    assert obj.length() == 3
    obj.array = Array()
    assert obj.length() == 3


def test_object_exceptions():
    obj = JSON.from_file(OBJECT_INPUT)

    with raises(TypeError, message="assign(*others) arguments must be instances of 'dict'"):
        obj.assign(None)

    with raises(TypeError, message="merge(*others) arguments must be instances of 'dict'"):
        obj.merge(None)

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
    obj1 = Object({"key": "value"})
    obj1_dc = obj1.deepcopy()
    obj2 = Object({"key": {"key": "value"}})
    obj2_dc = obj2.deepcopy()
    obj3 = obj1.assign(obj2)

    assert obj1 != obj1_dc
    assert obj2 == obj2_dc
    assert obj1 == obj2
    assert obj1 is obj3
    assert obj2 == obj3
    assert obj2 is not obj3
    assert obj2.key is obj3.key


def test_object_assign_pure():
    obj1 = Object({"key": "value"})
    obj1_dc = obj1.deepcopy()
    obj2 = Object({"key": {"key": "value"}})
    obj2_dc = obj2.deepcopy()
    obj3 = Object().assign(obj1, obj2)

    assert obj1 == obj1_dc
    assert obj2 == obj2_dc
    assert obj2 == obj3
    assert obj2 is not obj3
    assert obj2.key is obj3.key


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
    assert all(item in MAPPABLE_INT for item in obj.items(parse=True))
    assert all(item in MAPPABLE_INT for item in obj.items(parse=int))


def test_object_merge_mutate():
    obj1 = JSON.from_collection({"object": {"key1": "value1"}, "array": ["item1"]})
    obj1_dc = obj1.deepcopy()
    obj2 = JSON.from_collection({"array": ["item1", "item2"]})
    obj2_dc = obj2.deepcopy()
    obj3 = JSON.from_collection({"object": {"key1": "value1", "key2": "value2"}})
    obj3_dc = obj3.deepcopy()
    obj4 = JSON.from_collection({"object": {"key1": "value1", "key2": "value2"}, "array": ["item1", "item2"]})
    obj5 = obj1.merge(obj2, obj3)

    assert obj1 != obj1_dc
    assert obj2 == obj2_dc
    assert obj3 == obj3_dc
    assert obj4 == obj5
    assert obj4 is not obj5
    assert obj1 == obj5
    assert obj1 is obj5
    assert obj3.object == obj5.object
    assert obj3.object is not obj5.object


def test_object_merge_pure():
    obj1 = JSON.from_collection({"object": {"key1": "value1"}, "array": ["item1"]})
    obj1_dc = obj1.deepcopy()
    obj2 = JSON.from_collection({"array": ["item1", "item2"]})
    obj2_dc = obj2.deepcopy()
    obj3 = JSON.from_collection({"object": {"key1": "value1", "key2": "value2"}})
    obj3_dc = obj3.deepcopy()
    obj4 = JSON.from_collection({"object": {"key1": "value1", "key2": "value2"}, "array": ["item1", "item2"]})
    obj5 = Object().merge(obj1, obj2, obj3)

    assert obj1 == obj1_dc
    assert obj2 == obj2_dc
    assert obj3 == obj3_dc
    assert obj4 == obj5
    assert obj4 is not obj5
    assert obj3.object == obj5.object
    assert obj3.object is not obj5.object


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
