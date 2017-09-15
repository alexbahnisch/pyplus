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
        return iter([0, 1, 2, 3, 4, 5])


def test_isintlike():
    is_int = IsIntLike()
    assert isintlike(is_int)
    assert isintlike(1)
    assert isintlike(1.5)
    assert isintlike("1")
    assert isintlike(True)


def test_isintlike_not():
    assert not isintlike(None)
    assert not isintlike(OBJECT)
    assert not isintlike(SET)
    assert not isintlike(STRING)


def test_isiterable():
    is_iter = IsIterable()
    assert isiterable(is_iter)
    assert isiterable(DICT)
    assert isiterable(SET)
    assert isiterable(STRING)


def test_notiterable():
    assert not isiterable(OBJECT)
    assert not isiterable(1)
    assert not isiterable(1.5)
    assert not isiterable(True)
    assert not isiterable(None)


if __name__ == "__main__":
    pass
