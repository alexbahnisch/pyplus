#!/usr/bin/env python
from pyplus.data import dataobject, DataObjectMixin
from pyplus.test import assert_exception


@dataobject("index", "name", "value")
class Object1(object):
    def __init__(self, index, name, value):
        self.index = index
        self.name = name
        self.value = value

    def __eq__(self, other):
        try:
            return self.index == other.index and self.name == other.name and self.value == other.value
        except AttributeError:
            return False


class Object2(DataObjectMixin):
    __HEADERS__ = ["index", "name", "value"]

    def __init__(self, index, name, value):
        self.index = index
        self.name = name
        self.value = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.index == other.index and self.name == other.name and self.value == other.value
        else:
            return False


def test_dataobject():
    object1 = Object1(1, "object", 1.1)
    assert object1 == Object1.from_array([1, "object", 1.1])
    assert object1 == object1.from_json({"index": 1, "name": "object", "value": 1.1})

    assert_exception(Object1.from_line, AttributeError)
    assert_exception(object1.from_line, AttributeError)

    object2 = Object2(1, "object", 1.1)
    assert object2 == Object2.from_array([1, "object", 1.1])
    assert object2 == object2.from_json({"index": 1, "name": "object", "value": 1.1})

    assert_exception(Object2.from_line, AttributeError)
    assert_exception(object2.from_line, AttributeError)


if __name__ == "__main__":
    test_dataobject()
