#!/usr/bin/env python
from pyplus.data import dataobject, DataObjectMixin


@dataobject("index", "name", "value")
class Object1:
    def __init__(self, index, name, value):
        self._index = index
        self._name = name
        self._value = value


class Object2(DataObjectMixin):
    __HEADERS__ = ["index", "name", "value"]

    def __init__(self, index, name, value):
        self._index = index
        self._name = name
        self._value = value


def test_dataobject():
    x11 = Object1.from_array([1, "object", 1.1])
    x12 = x11.from_json({"index": 1, "name": "object", "value": 1.1})

    try:
        x13 = Object1.from_line("")
        assert False
    except NotImplementedError:
        assert True

    x14 = Object1(1, "object", 1.1)

    x21 = Object2.from_array([1, "object", 1.1])
    x22 = x21.from_json({"index": 1, "name": "object", "value": 1.1})

    try:
        x23 = Object2.from_line("")
        assert False
    except NotImplementedError:
        assert True

    x24 = Object2(1, "object", 1.1)

    print()


if __name__ == "__main__":
    test_dataobject()
