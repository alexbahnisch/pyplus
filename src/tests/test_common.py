#!/usr/bin/env python
from pyplus.common import *


DICT = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
LIST = [1, 2, 3, 4, 5]
MAPPABLE = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
OBJECT = object()
SET = {1, 2, 3, 4, 5}
STRING = "string"
TUPLE = [1, 2, 3, 4, 5]


class IsIntLike(object):
    def __int__(self):
        return 1


class IsIterable(object):
    def __iter__(self):
        return iter(LIST)


class IsListLike(object):
    def __getitem__(self, item):
        return 1

    def __iter__(self):
        return iter(LIST)

    def __len__(self):
        return 5

    def __setitem__(self, key, value):
        pass


class IsPair(object):
    def __getitem__(self, item):
        return 1

    def __len__(self):
        return 2


def test_isintlike():
    assert isintlike(1)
    assert isintlike(1.5)
    assert isintlike("1")
    assert isintlike(False)
    assert isintlike(IsIntLike())


def test_isintlike_not():
    assert not isintlike(None)
    assert not isintlike(OBJECT)
    assert not isintlike(SET)
    assert not isintlike(STRING)


def test_isiterable():
    assert isiterable(DICT)
    assert isiterable(IsIterable())
    assert isiterable(LIST)
    assert isiterable(MAPPABLE)
    assert isiterable(SET)
    assert isiterable(TUPLE)


def test_isiterable_not():
    assert not isiterable(1)
    assert not isiterable(1.5)
    assert not isiterable(False)
    assert not isiterable(None)
    assert not isiterable(OBJECT)
    assert not isiterable(STRING)


def test_islistlike():
    assert islistlike(DICT)
    assert islistlike(IsListLike())
    assert islistlike(LIST)
    assert islistlike(MAPPABLE)
    assert islistlike(TUPLE)


def test_islistlike_not():
    assert not islistlike(1)
    assert not islistlike(1.5)
    assert not islistlike(False)
    assert not islistlike(None)
    assert not islistlike(OBJECT)
    assert not islistlike(SET)
    assert not islistlike(STRING)


def test_ispair():
    pass


def test_ispair_not():
    pass


if __name__ == "__main__":
    pass
