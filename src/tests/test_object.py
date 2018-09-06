#!/usr/bin/env python3
from pyplus.object import *
from pyplus.path import LazyPath
from pytest import raises

DIR = LazyPath(__file__)
CSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/csv/headers.csv")
CSV_HEADERS_OUTPUT = LazyPath(DIR.parent, "../resources/csv/headers.output.csv")
CSV_HEADERS_TEMP = LazyPath(DIR.parent, "../resources/csv/headers.temp.csv")
CSV_HEADLESS_OUTPUT = LazyPath(DIR.parent, "../resources/csv/headless.output.csv")
CSV_HEADLESS_TEMP = LazyPath(DIR.parent, "../resources/csv/headless.temp.csv")
TSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headers.tsv")
TSV_HEADERS_OUTPUT = LazyPath(DIR.parent, "../resources/tsv/headers.output.tsv")
TSV_HEADERS_TEMP = LazyPath(DIR.parent, "../resources/tsv/headers.temp.tsv")
TSV_HEADLESS_OUTPUT = LazyPath(DIR.parent, "../resources/tsv/headless.output.tsv")
TSV_HEADLESS_TEMP = LazyPath(DIR.parent, "../resources/tsv/headless.temp.tsv")


# noinspection PyUnresolvedReferences
def test_lazy_object_copy():
    obj = LazyObject(key1=[1, 2])
    obj_copy = obj.copy()
    obj_deepcopy = obj.deepcopy()

    assert obj == obj_copy
    assert obj is not obj_copy
    assert obj.key1 is obj_copy.key1

    assert obj == obj_deepcopy
    assert obj is not obj_deepcopy
    assert obj.key1 == obj_deepcopy.key1
    assert obj.key1 is not obj_deepcopy.key1


def test_lazy_object_eq():
    obj1 = LazyObject(key1=1, key2=2)
    obj2 = ImmutableLazyObject(key1=1, key2=2)

    assert obj1 == {"key1": 1, "key2": 2}
    assert obj1 == obj2
    assert obj1 is not obj2


def test_lazy_object_extendable():
    obj1 = LazyObject(key1=1, key2=2, key3=3)
    obj2 = AssignableLazyObject(key1=1, key2=2)
    assert obj1 != obj2

    obj2.key3 = 3
    assert obj1 == obj2


def test_lazy_object_exception():
    with raises(AttributeError, message="'Object' object has no attribute 'key3'"):
        obj = LazyObject(key1=1, key2=2)
        obj.key2 = 2
        obj.key3 = 3

    with raises(AttributeError, message="can't set attribute 'key2', 'ImmutableObject' instances are immutable"):
        obj = ImmutableLazyObject(key1=1, key2=2)
        obj.key2 = 2

    with raises(TypeError, message="'path' argument must be a bytes or unicode string or pathlib.Path"):
        LazyObjects.from_table(object())


def test_lazy_object_hash():
    obj1 = LazyObject(key1=1, key2=2)
    obj2 = LazyObject(key1=1, key2=2)
    obj = obj1
    dictionary = {obj1: 1, obj2: 2}

    assert dictionary[obj1] == 1
    assert dictionary[obj2] == 2
    assert obj is obj1
    assert hash(obj) == hash(obj1)
    assert obj is not obj2
    assert hash(obj) != hash(obj2)


def test_lazy_object_ne():
    obj1 = LazyObject(key1=1, key2=2)
    obj2 = ImmutableLazyObject(key1=2, key2=1)

    assert obj1 != obj2
    assert obj1 != 1


def test_lazy_object_repr():
    assert repr(LazyObject(key1=1)) == "LazyObject(key1=1)"
    assert repr(LazyObject(key1=1, key2=2)) == "LazyObject(key1=1, key2=2)" or repr(
        LazyObject(key1=1, key2=2)) == "LazyObject(key2=2, key1=1)"


def test_lazy_objects():
    obj1 = LazyObject(param=1)
    obj2 = AssignableLazyObject(param=1)
    obj3 = ImmutableLazyObject(param=1)
    obj4 = obj1.copy()

    objects = LazyObjects()
    objects.push(obj1, obj2, obj3)

    assert objects.length() == 3
    assert obj1 in objects
    assert obj4 not in objects

    objects.push(obj1)
    assert objects.length() == 3

    objects.push(obj4)
    assert objects.length() == 4

    assert objects[0] is obj1
    assert objects[1] is obj2
    assert objects[2] is obj3
    assert objects[3] is obj4

    assert repr(objects) == repr(list(objects))


# noinspection PyUnresolvedReferences
def test_lazy_objects_copy():
    obj = LazyObject(key1=[1, 2])
    objects = LazyObjects([obj])
    objects_copy = objects.copy()
    objects_deepcopy = objects.deepcopy()

    assert objects == objects_copy
    assert objects is not objects_copy
    assert objects[0] is objects_copy[0]

    assert objects == objects_deepcopy
    assert objects is not objects_deepcopy
    assert objects[0] == objects_deepcopy[0]
    assert objects[0] is not objects_deepcopy[0]
    assert objects[0].key1 == objects_deepcopy[0].key1
    assert objects[0].key1 is not objects_deepcopy[0].key1


def test_lazy_objects_eq():
    obj1 = LazyObject(param=1)
    obj2 = AssignableLazyObject(param=2)
    obj3 = ImmutableLazyObject(param=3)
    objects = LazyObjects([obj1, obj2, obj3])

    assert objects == [obj1, obj2, obj3]
    assert objects == [obj1.copy(), obj2.copy(), obj3.copy()]


def test_lazy_objects_exception():
    with raises(TypeError, message="'NoneType' object is not an instance of LazyObject"):
        objects = LazyObjects()
        objects.push(None)

    with raises(TypeError, message="'NoneType' object is not iterable"):
        LazyObjects(LazyObject(key1=1))

    with raises(TypeError, message="'path' argument must be a bytes or unicode string or pathlib.Path"):
        objects = LazyObjects()
        objects.to_table(None)


def test_lazy_objects_ne():
    obj1 = LazyObject(param=1)
    obj2 = AssignableLazyObject(param=2)
    obj3 = ImmutableLazyObject(param=3)
    objects = LazyObjects([obj1, obj2, obj3])

    assert objects != [obj3, obj2, obj1]
    assert objects != [obj1, obj2]
    assert objects != obj1


def test_lazy_objects_table():
    objects1 = LazyObjects.from_table(CSV_HEADERS_INPUT)
    objects1.to_table(CSV_HEADERS_TEMP)
    assert LazyObjects.from_table(CSV_HEADERS_OUTPUT) == LazyObjects.from_table(CSV_HEADERS_TEMP)

    objects2 = LazyObjects.from_table(TSV_HEADERS_INPUT, delimiter="\t")
    objects2.to_table(TSV_HEADERS_TEMP, delimiter="\t")
    assert LazyObjects.from_table(TSV_HEADERS_OUTPUT, delimiter="\t") == LazyObjects.from_table(TSV_HEADERS_TEMP,
                                                                                                delimiter="\t")
    assert objects1 == objects2
