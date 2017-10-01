#!/usr/bin/env python
from pyplus.object import *
from pyplus.path import LazyPath
from pytest import raises

DIR = LazyPath(__file__)
CSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/csv/headers.csv")
CSV_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/csv/headless.csv")
TSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headers.tsv")
TSV_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headless.tsv")


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
    assert repr(LazyObject(key1=1, key2=2)) == "LazyObject(key1=1, key2=2)" or repr(LazyObject(key1=1, key2=2)) == "LazyObject(key2=2, key1=1)"


def test_lazy_objects_headers():
    objects1 = LazyObjects.from_table(CSV_HEADERS_INPUT, delimiter=",")
    objects2 = LazyObjects.from_table(TSV_HEADERS_INPUT, delimiter="\t")
    assert objects1 == objects2


def test_lazy_objects_headless():
    objects1 = LazyObjects.from_table(CSV_HEADLESS_INPUT, delimiter=",")
    objects2 = LazyObjects.from_table(TSV_HEADLESS_INPUT, delimiter="\t")
    assert objects1 == objects2
